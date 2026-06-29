from qdrant_client import QdrantClient
from app.core.config import settings
from langchain_qdrant import QdrantVectorStore
from app.ingestion.ingester import embedder
from qdrant_client.models import VectorParams, Distance

# COLLECTION NAME
COLLECTION_NAME = "company_knowledge"


# QDRANT CLIENT INSTANCE
client = QdrantClient(
    api_key=settings.QDRANT_API_KEY,
    url=settings.QDRANT_URL,
)


# ===========================
# VECTOR DATABASE FUCNTIONS
# ===========================
def create_collection_if_missing():
    exists = client.collection_exists(
        collection_name=COLLECTION_NAME,
    )

    if not exists:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=384,
                distance=Distance.COSINE,
            ),
        )


def collection_exists() -> bool:
    exists = client.collection_exists(
        collection_name=COLLECTION_NAME,
    )

    return exists


# CREATE COLLECTION IF NOT EXISTS
create_collection_if_missing()

# QDRANT VECTOR DB INSTANCE
qdrant_db = QdrantVectorStore(
    client=client,
    collection_name=COLLECTION_NAME,
    embedding=embedder,
)
