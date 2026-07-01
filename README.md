# 📄 Chat with PDF using Retrieval-Augmented Generation (RAG)

An AI-powered application that allows users to upload a PDF and ask questions in natural language. The application uses a Retrieval-Augmented Generation (RAG) pipeline to retrieve relevant information from the uploaded document before generating responses with Mistral AI, ensuring answers are grounded in the document's content.

---

## ✨ Features

- Upload and process PDF documents
- Ask questions in natural language
- Context-aware responses based only on the uploaded PDF
- Semantic search using vector embeddings
- Interactive Streamlit interface

---

## 🛠️ Tech Stack

| Category | Technologies |
|----------|--------------|
| Language | Python |
| Framework | Streamlit |
| LLM | Mistral AI |
| AI Framework | LangChain |
| Vector Database | ChromaDB |
| Document Processing | PyPDFLoader |
| Embeddings | Sentence Transformers |

---

## ⚙️ Workflow

```text
PDF Upload
    │
    ▼
Document Processing
    │
    ▼
Text Chunking
    │
    ▼
Vector Embeddings
    │
    ▼
ChromaDB
    │
    ▼
Semantic Retrieval
    │
    ▼
Mistral AI
    │
    ▼
Generated Response
```

---

## 💡 Design Decisions

- Implemented a Retrieval-Augmented Generation (RAG) pipeline to generate responses grounded in the uploaded document instead of relying solely on the LLM's pre-trained knowledge.
- Used ChromaDB for efficient vector storage and semantic similarity search.
- Built the user interface with Streamlit for rapid development and an intuitive user experience.

---

## 🚧 Current Status

This project is under active development. Future improvements include:

- Multi-document support
- Conversation history
- Source citations for generated answers
- Enhanced retrieval techniques
- Cloud deployment

---

## 📚 What I Learned

- Retrieval-Augmented Generation (RAG)
- Large Language Model (LLM) Integration
- Prompt Engineering
- Vector Databases
- Semantic Search
- Building AI Applications with Streamlit

---
