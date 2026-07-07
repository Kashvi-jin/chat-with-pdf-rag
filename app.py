# import os
import tempfile
# import shutil

import streamlit as st
from dotenv import load_dotenv

from pypdf import PdfReader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_community.vectorstores import Chroma
from langchain_mistralai import MistralAIEmbeddings
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

st.set_page_config(
    page_title="RAG PDF Chat",
    page_icon="📚",
    layout="wide"
)

st.title("📚 Chat with your PDF")

st.write("Upload any PDF and ask questions about it.")

uploaded_file = st.file_uploader(
    "Upload a PDF",
    type=["pdf"]
)

# persist_directory = "Chroma_db"

embedding_model = MistralAIEmbeddings()

llm = ChatMistralAI(
    model="mistral-small-2603"
)


prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are a helpful AI assistant.

Use ONLY the provided context to answer the user's question.

If the answer is not present in the context, reply:

"I could not find the answer in the document."
"""
        ),
        (
            "human",
            """
Context:
{context}

Question:
{question}
"""
        )
    ]
)

# ----------------------------
# Build Vector Database
# ----------------------------

if uploaded_file:

    if st.button("Process PDF"):

#         if os.path.exists(persist_directory):
#             shutil.rmtree(persist_directory)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.read())
            pdf_path = tmp_file.name

#         with st.spinner("Reading PDF..."):

            reader = PdfReader(pdf_path)


            docs = []

            for i, page in enumerate(reader.pages):
                text = page.extract_text() or ""

                docs.append(
                    Document(
                        page_content=text,
                        metadata={"page": i + 1}
                    )
                )

            st.write(f"Loaded {len(docs)} pages")

            # splitter = RecursiveCharacterTextSplitter(
            #     chunk_size=1000,
            #     chunk_overlap=200
            # )

            # chunks = splitter.split_documents(docs)
            # st.write(f"Created {len(chunks)} chunks")

#             Chroma.from_documents(
#                 documents=chunks,
#                 embedding=embedding_model,
#                 persist_directory=persist_directory
#             )

#         os.remove(pdf_path)

        st.success("PDF processed successfully!")

# # ----------------------------
# # Chat
# # ----------------------------

# if os.path.exists(persist_directory):

#     vectorstore = Chroma(
#         persist_directory=persist_directory,
#         embedding_function=embedding_model
#     )

#     retriever = vectorstore.as_retriever(
#         search_type="mmr",
#         search_kwargs={
#             "k":4,
#             "fetch_k":10,
#             "lambda_mult":0.5
#         }
#     )

#     question = st.text_input("Ask a question")

#     if st.button("Ask"):

#         with st.spinner("Thinking..."):

#             docs = retriever.invoke(question)

#             context = "\n\n".join(
#                 [doc.page_content for doc in docs]
#             )

#             final_prompt = prompt.invoke(
#                 {
#                     "context": context,
#                     "question": question
#                 }
#             )

#             response = llm.invoke(final_prompt)

#             st.markdown("### Answer")

#             st.write(response.content)

#             with st.expander("Retrieved Context"):

#                 for i, doc in enumerate(docs, 1):
#                     st.markdown(f"### Chunk {i}")
#                     st.write(doc.page_content)