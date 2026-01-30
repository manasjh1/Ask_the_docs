# Ask the Docs

*A Retrieval-Augmented Generation (RAG) Application for Document Question Answering*

## Live Demo

🔗 **Live Application:** [https://askdocsgroup-gtgsecb4ewg2gtep.canadacentral-01.azurewebsites.net/](https://askdocsgroup-gtgsecb4ewg2gtep.canadacentral-01.azurewebsites.net/)
*(Hosted on Azure Web Apps using Docker containers)*

---

## Overview

Ask the Docs is a Retrieval-Augmented Generation (RAG)–based application that enables users to ask natural-language questions over static documents such as PDFs and text files. Instead of manually searching through large documents, the system retrieves semantically relevant content and generates accurate, context-aware answers using a Large Language Model (LLM).

The application ensures that responses are strictly grounded in the uploaded documents, reducing hallucinations and improving answer reliability.

---

## Key Features

* Upload and query PDF or text documents
* Semantic search using vector embeddings
* Context-grounded answer generation using an LLM
* Low-latency inference via Groq
* Persistent and scalable vector storage
* Fully containerized and cloud-deployed

---

## System Architecture

The system follows a microservices-based, containerized architecture:

* **Frontend**: Streamlit for document upload and querying
* **Backend**: FastAPI for ingestion, retrieval, and orchestration
* **LLM**: Llama-3-70B served via Groq
* **Embeddings**: HuggingFace sentence-transformer models
* **Vector Database**:

  * Pinecone (production)
  * FAISS (local development fallback)
* **Deployment**: Docker containers hosted on Azure Web Apps

---

## Workflow

### Document Ingestion

1. User uploads a PDF or text file
2. Text is extracted and split into manageable chunks
3. Each chunk is converted into a semantic embedding
4. Embeddings are stored in the vector database

### Question Answering

1. User submits a natural-language query
2. The query is embedded using the same embedding model
3. Relevant document chunks are retrieved via semantic search
4. A constrained prompt is constructed
5. The LLM generates an answer strictly based on retrieved context

---

## Vector Database Strategy

* **FAISS**
  Used during local development for fast and simple similarity search.
  Not suitable for production due to lack of persistence and scalability.

* **Pinecone**
  Used in production for persistent, scalable, and stateless vector storage, enabling reliable multi-user access and cloud deployment.

---

## Deployment

* Containerized using Docker with a multi-stage build
* CPU-only PyTorch configuration to reduce image size and cost
* Docker Compose used to manage frontend and backend services
* Deployed on Azure Web Apps for Containers
* Secrets managed securely using environment variables

---

## Technology Stack

| Component        | Technology         |
| ---------------- | ------------------ |
| Frontend         | Streamlit          |
| Backend          | FastAPI            |
| LLM Inference    | Groq (Llama-3-70B) |
| Embeddings       | HuggingFace        |
| Vector Database  | Pinecone           |
| Containerization | Docker             |
| Cloud Platform   | Azure Web Apps     |

---

## Use Cases

* Internal company documentation search
* Policy and handbook question answering
* Academic or research document exploration
* Knowledge-base assistants

---

## Future Improvements

* OCR support for scanned documents
* User authentication and document isolation
* Hybrid search (keyword + vector)
* Conversation memory and chat history
* Evaluation metrics for retrieval accuracy

---

## License

This project is intended for educational and demonstration purposes.


