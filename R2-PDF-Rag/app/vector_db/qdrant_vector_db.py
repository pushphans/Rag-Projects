from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from app.core.config import settings
from langchain_qdrant import QdrantVectorStore
from app.rag.ingestion_pipeline.embedder import embedder

collection_name = "pdf_collection"


# QDRANT CLIENT
QClient = QdrantClient(
    api_key=settings.QDRANT_API_KEY,
    url=settings.QDRANT_URL,
)


try:
    if not QClient.collection_exists(collection_name=collection_name):
        QClient.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(
                size=384,
                distance=Distance.COSINE,
            ),
        )

except Exception as e:
    print(f"--- ⚠️ Collection check/creation failed: {str(e)} ---")


# QDRANT VECTOR DB
QVectorDb = QdrantVectorStore(
    client=QClient,
    collection_name=collection_name,
    embedding=embedder,
)
