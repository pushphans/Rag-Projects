# R1-Text-Rag

A text-based **Retrieval-Augmented Generation** pipeline that ingests plain text files, indexes them in a local **Chroma** vector store, and answers questions using **DeepSeek Chat** via a **LangGraph** workflow.

## Tech Stack

- **Framework:** FastAPI + Uvicorn
- **LLM:** DeepSeek Chat (`deepseek-chat`)
- **Embeddings:** `sentence-transformers/all-MiniLM-L6-v2` (384-dim)
- **Vector Store:** Chroma (local, on-disk)
- **Workflow:** LangGraph StateGraph

## Setup

```bash
cd R1-Text-Rag
python -m venv .venv
.venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

Create a `.env` file:

```
DEEPSEEK_API_KEY=your_key_here
```

## Usage

Start the server:

```bash
uvicorn app.main:app --reload
```

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/rag/ingest` | Load, chunk, embed, and store `sample.txt` |
| `POST` | `/rag/query` | Ask a question — returns LLM answer with retrieved context |

**Query example:**

```json
{
  "question": "What is Google known for?"
}
```

## Project Structure

```
R1-Text-Rag/
├── app/
│   ├── main.py
│   ├── core/config.py
│   ├── api/router.py
│   └── rag/
│       ├── loader.py
│       ├── splitter.py
│       ├── embedder.py
│       ├── vector_db.py
│       └── retreival_workflow/
│           ├── rag_state.py
│           └── rag_graph.py
├── requirements.txt
└── pyproject.toml
```
