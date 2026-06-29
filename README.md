# Enterprise Knowledge Assistant

*A Production-Oriented Retrieval-Augmented Generation (RAG) System for Enterprise Document Question Answering*

## Overview

The Enterprise Knowledge Assistant is an AI-powered question-answering system that enables users to interact with enterprise documents using natural language. The application implements a Retrieval-Augmented Generation (RAG) pipeline that retrieves relevant information from a document knowledge base and generates grounded responses using Google's Gemini 2.5 Flash model.

Unlike a simple chatbot, the system is designed with a modular, production-oriented architecture. It separates document ingestion, indexing, retrieval, prompt construction, and response generation into independent components, making the application easier to maintain, extend, and evaluate.

The project was developed as part of the Anthrasync AI Engineer technical assessment to demonstrate practical AI engineering skills, including document processing, semantic search, vector databases, LLM integration, API development, and software engineering best practices.

## Features

* Multi-format document ingestion (PDF, DOCX, TXT, Markdown)
* Modular document processing pipeline
* Metadata extraction and intelligent text chunking
* Semantic vector search using FAISS
* Sentence embeddings using **BAAI/bge-small-en-v1.5**
* Grounded answer generation using **Google Gemini 2.5 Flash**
* Source citation with document, page, and section references
* Confidence estimation based on retrieval distance
* REST API built with FastAPI
* Interactive Streamlit user interface
* Docker support for containerized deployment
* Modular architecture following separation of concerns
* Configuration through environment variables
* Structured logging and typed request/response schemas

## System Architecture

The application follows a modular layered architecture in which each component has a single responsibility.

1. Documents are ingested through a custom document processing pipeline supporting multiple file formats.
2. Documents are cleaned, enriched with metadata, and split into semantic chunks.
3. Text chunks are converted into dense vector embeddings using the BAAI/bge-small-en-v1.5 embedding model.
4. Embeddings are indexed in a FAISS vector database for efficient similarity search.
5. User questions are embedded and matched against the indexed document chunks through semantic retrieval.
6. Retrieved context is assembled into a structured RAG prompt.
7. Google Gemini 2.5 Flash generates grounded answers using only the retrieved context.
8. The API returns the generated answer together with source citations, retrieval confidence, and processing latency.

## Project Structure

```text
Enterprise_knowledge_assistant/
│
├── app/
│   ├── api/                # FastAPI routes
│   ├── config/             # Application configuration & logging
│   ├── ingestion/          # Document loaders, cleaning, metadata extraction
│   ├── llm/                # Gemini provider and provider factory
│   ├── models/             # Internal domain models
│   ├── prompts/            # Prompt templates
│   ├── retrieval/          # FAISS indexing and retrieval
│   ├── schemas/            # API request/response schemas
│   ├── scripts/            # Utility scripts (index building, testing)
│   ├── services/           # Business logic orchestration
│   └── main.py             # FastAPI application entry point
│
├── frontend/
│   └── streamlit_app.py    # Streamlit user interface
│
├── data/
│   ├── documents/          # Input enterprise documents
│   └── vector_store/       # Generated FAISS index
│
├── docs/
│   └── system_design.md
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── README.md
```

## Technology Stack

| Category             | Technology                     |
| -------------------- | ------------------------------ |
| Programming Language | Python 3.11                    |
| Backend API          | FastAPI                        |
| Frontend             | Streamlit                      |
| LLM                  | Google Gemini 2.5 Flash        |
| Embedding Model      | BAAI/bge-small-en-v1.5         |
| Vector Database      | FAISS                          |
| AI Framework         | LangChain                      |
| Document Processing  | PyMuPDF, python-docx, Markdown |
| Data Validation      | Pydantic                       |
| Configuration        | pydantic-settings              |
| Containerization     | Docker & Docker Compose        |
| Logging              | Python Logging                 |


## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd Enterprise_knowledge_assistant
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate the environment:

**Windows**

```bash
.venv\Scripts\activate
```

**Linux / macOS**

```bash
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file using `.env.example`.

```env
GOOGLE_API_KEY=your_google_api_key
```

## Document Ingestion and Indexing

Place enterprise documents inside:

```text
data/documents/
```

Supported document formats:

* PDF
* DOCX
* TXT
* Markdown

Build the vector index:

```bash
python -m app.scripts.build_index
```

This pipeline performs:

* Document loading
* Text extraction
* Metadata extraction
* Intelligent text chunking
* Embedding generation
* FAISS vector index creation

## Running the Application

### Step 1 — Build the Knowledge Base

Before starting the application, generate the vector index from the enterprise documents.

```bash
python -m app.scripts.build_index
```

---

### Step 2 — Start the FastAPI Backend

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

---

### Step 3 — Start the Streamlit Frontend

```bash
streamlit run frontend/streamlit_app.py
```

The user interface will be available at:

```text
http://localhost:8501
```

## API Usage

### POST `/ask`

Accepts a natural language question and returns a grounded response generated using the RAG pipeline.

### Example Request

```json
{
    "question": "What are the evaluation criteria?"
}
```

### Example Response

```json
{
    "answer": "The evaluation criteria include AI System Design, Answer Quality, Engineering Quality, Evaluation Approach, and Documentation.",
    "sources": [
        {
            "document": "AI Engineer Assignment.pdf",
            "page": 6,
            "section": "Engineering Quality"
        }
    ],
    "confidence": 0.62,
    "retrieved_chunks": 5,
    "processing_time_ms": 2418.37
}
```

## Design Decisions

Several design decisions were made to keep the system modular, maintainable, and production-oriented.

### Why Retrieval-Augmented Generation (RAG)?

A RAG architecture was chosen instead of relying solely on a Large Language Model because enterprise knowledge changes frequently. Retrieving relevant document context before generation improves factual accuracy, reduces hallucinations, and allows the knowledge base to be updated without retraining the language model.

---

### Why FAISS?

FAISS provides efficient similarity search over dense vector embeddings and performs well for small to medium-sized enterprise document collections. It is lightweight, open source, and integrates well with LangChain.

---

### Why BAAI/bge-small-en-v1.5?

The BAAI embedding model provides high-quality semantic representations while remaining lightweight enough for local inference. It offers a good balance between retrieval quality and computational efficiency.

---

### Why Google Gemini 2.5 Flash?

Gemini 2.5 Flash was selected because it provides fast inference, strong reasoning capabilities, and an accessible API suitable for production-oriented question-answering systems.

---

### Why FastAPI?

FastAPI provides automatic request validation, OpenAPI documentation, and high-performance asynchronous APIs, making it well suited for AI applications.

---

### Why Streamlit?

Streamlit enables rapid development of an interactive interface for demonstrating AI applications without introducing unnecessary frontend complexity.

## Current Limitations

* The current implementation performs single-turn question answering and does not maintain conversational memory.
* The vector index must be rebuilt when documents are added or updated.
* Confidence scores are heuristic and based on retrieval distance rather than calibrated probabilities.
* The current retrieval pipeline uses semantic search only and does not include reranking or hybrid retrieval.

## Future Improvements

* Hybrid retrieval combining semantic search with keyword-based retrieval.
* Cross-encoder reranking to improve retrieval relevance.
* Incremental indexing for newly added documents.
* Conversation memory for multi-turn interactions.
* Role-based document access and authentication.
* Evaluation framework with automated retrieval and answer quality metrics.
* Support for additional enterprise document formats.
* Deployment using cloud-native infrastructure with scalable vector databases.

## Performance and Evaluation

The system was evaluated using representative questions derived from the provided enterprise documents.

The evaluation focused on:

* Retrieval relevance
* Answer correctness
* Grounding to retrieved context
* Source citation accuracy
* Hallucination prevention
* API response latency

Testing was performed through both the FastAPI endpoint and the Streamlit interface. The modular architecture also allows each component (document ingestion, retrieval, and LLM generation) to be tested independently.

## Docker Support

The project includes Docker and Docker Compose configurations for containerized deployment.

Build and start the application:

```bash
docker compose up --build
```

The API will be available on:

```text
http://localhost:8000
```

The Streamlit UI will be available on:

```text
http://localhost:8501
```

> **Note:** Before starting the containers, ensure the document vector index has been generated. If using Docker with a locally generated FAISS index, mount the `data/` directory or rebuild the index inside the container.

## Author

**Shashank Sharma**

AI & Machine Learning Engineer

For questions regarding the implementation or design decisions, please feel free to reach out through the contact information provided with the project submission.

## Acknowledgements

This project leverages several outstanding open-source technologies, including FastAPI, Streamlit, LangChain, FAISS, Hugging Face sentence-transformers, and Google's Gemini API. Their contributions make rapid development of production-oriented AI applications possible.

## Additional Documentation

A detailed **System Design Document** describing the system architecture, data flow, design decisions, and scalability considerations is available in the `docs/` directory.