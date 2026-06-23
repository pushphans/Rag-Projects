from langchain_chroma import Chroma
from pathlib import Path

from app.rag.splitter import chunked_docs
from app.rag.embedder import embedder


persist_dir = Path("app/rag/chroma_db").resolve()



if persist_dir.exists():
    print("Loading existing vector database...")
    vector_db = Chroma(
        embedding_function= embedder,
        persist_directory = persist_dir
    )
else:
    vector_db = Chroma.from_documents(
        documents= chunked_docs,
        embedding= embedder,
        persist_directory = persist_dir
)

