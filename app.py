import os
import tempfile
import streamlit as st
from dotenv import load_dotenv

from pypdf import PdfReader
from langchain_core.documents import Document
from langchain_mistralai import MistralAIEmbeddings, ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate

# Naya package import jo crash nahi hoga
from langchain_chroma import Chroma

load_dotenv()

st.set_page_config(
    page_title="RAG PDF Chat",
    page_icon="📚",
    layout="wide"
)

st.title("📚 Chat with your PDF")
st.write("Upload any PDF and ask questions about it.")

if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None

uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful AI assistant.\n\nUse ONLY the provided context to answer the user's question.\n\nIf the answer is not present in the context, reply:\n\"I could not find the answer in the document.\""),
    ("human", "Context:\n{context}\n\nQuestion:\n{question}")
])

# Fail-safe Text Splitter using pure Python loops (Zero Import Crash)
def safe_split_text(docs, chunk_size=1000, chunk_overlap=200):
    chunks = []
    for doc in docs:
        text = doc.page_content
        start = 0
        while start < len(text):
            end = start + chunk_size
            chunk_text = text[start:end]
            chunks.append(Document(page_content=chunk_text, metadata=doc.metadata))
            start += chunk_size - chunk_overlap
    return chunks

# ----------------------------
# Build Vector Database
# ----------------------------
if uploaded_file:
    if st.button("Process PDF"):
        with st.spinner("Processing PDF, please wait..."):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(uploaded_file.read())
                pdf_path = tmp_file.name

            try:
                reader = PdfReader(pdf_path)
                docs = []

                for i, page in enumerate(reader.pages):
                    text = page.extract_text() or ""
                    docs.append(Document(page_content=text, metadata={"page": i + 1}))

                st.write(f"Loaded {len(docs)} pages")

                # Text split bina kisi crash ke
                chunks = safe_split_text(docs)
                st.write(f"Created {len(chunks)} chunks")

                embedding_model = MistralAIEmbeddings()
                
                # CHROMA USE HO RAHA HAI YAHAN (In-memory mode, safe on Windows)
                st.session_state.vectorstore = Chroma.from_documents(
                    documents=chunks,
                    embedding=embedding_model
                )
                st.success("PDF processed successfully with Chroma!")

            except Exception as e:
                st.error(f"Error during Chroma processing: {e}")
            finally:
                if os.path.exists(pdf_path):
                    os.remove(pdf_path)

# ----------------------------
# Chat Interface
# ----------------------------
if st.session_state.vectorstore is not None:
    st.write("---")
    retriever = st.session_state.vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={"k": 4, "fetch_k": 10, "lambda_mult": 0.5}
    )

    question = st.text_input("Ask a question")

    if st.button("Ask"):
        if question:
            with st.spinner("Thinking..."):
                llm = ChatMistralAI(model="mistral-small-2603")
                docs = retriever.invoke(question)
                context = "\n\n".join([doc.page_content for doc in docs])
                final_prompt = prompt.invoke({"context": context, "question": question})
                response = llm.invoke(final_prompt)

                st.markdown("### Answer")
                st.write(response.content)
        else:
            st.warning("Please type a question first.")