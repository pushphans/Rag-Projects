# R3-Company-Knowledge-Rag-Bot

A PDF-based **Retrieval-Augmented Generation** system for company knowledge documents. Upload PDFs, chunk and embed them into a **Qdrant** vector store, and retrieve relevant sections via semantic search.

## Tech Stack

- **Framework:** FastAPI + Uvicorn
- **Embeddings:** `sentence-transformers/all-MiniLM-L6-v2` (384-dim)
- **Vector Store:** Qdrant (cloud-hosted)
- **PDF Parsing:** PyMuPDF / pypdf

## Setup

```bash
cd R3-Company-Knowledge-Rag-Bot
python -m venv .venv
.venv\Scripts\activate     # Windows
pip install -r requirement.txt
```

Create a `.env` file:

```
DEEPSEEK_API_KEY=your_key_here
QDRANT_URL=https://your-cluster.cloud.qdrant.io
QDRANT_API_KEY=your_qdrant_key_here
```

## Usage

Start the server:

```bash
uvicorn app.main:app --reload
```

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/rag/upload` | Upload a PDF file — parses, chunks, embeds, and stores in Qdrant |
| `POST` | `/rag/retrieve` | Query semantic search — returns top-5 relevant chunks |
| `DELETE` | `/rag/delete` | Delete the Qdrant collection |

**Upload example:**

```bash
curl -X POST -F "file=@document.pdf" http://localhost:8000/rag/upload
```

**Retrieve example:**

```bash
curl "http://localhost:8000/rag/retrieve?query=company+policies"
```

## Project Structure

```
R3-Company-Knowledge-Rag-Bot/
├── app/
│   ├── main.py
│   ├── core/config.py
│   ├── api/rag_router.py
│   ├── ingestion/ingester.py
│   ├── retriever/retriever.py
│   └── vector_db/qdrant.py
├── requirement.txt
└── pyproject.toml
```
