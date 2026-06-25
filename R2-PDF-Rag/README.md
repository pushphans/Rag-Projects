# R2-PDF-Rag

A PDF-based **Retrieval-Augmented Generation** pipeline that ingests PDF documents, indexes them in a cloud **Qdrant** vector store, and provides a foundation for answering questions with **DeepSeek Chat**.

## Tech Stack

- **Framework:** FastAPI + Uvicorn
- **LLM:** DeepSeek Chat (`deepseek-chat`)
- **Embeddings:** `sentence-transformers/all-MiniLM-L6-v2` (384-dim)
- **Vector Store:** Qdrant (cloud-hosted)

## Setup

```bash
cd R2-PDF-Rag
python -m venv .venv
.venv\Scripts\activate     # Windows
pip install -r requirements.txt
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
| `POST` | `/rag/ingest` | Load, chunk, embed, and store `sample.pdf` into Qdrant |

## Project Structure

```
R2-PDF-Rag/
├── app/
│   ├── main.py
│   ├── core/config.py
│   ├── api/rag_router.py
│   ├── rag/
│   │   └── ingestion_pipeline/
│   │       ├── ingestion.py
│   │       └── embedder.py
│   └── vector_db/
│       └── qdrant_vector_db.py
├── sample_data/sample.pdf
├── requirements.txt
└── pyproject.toml
```
