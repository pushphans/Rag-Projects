from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from langchain_qdrant import QdrantVectorStore
from app.core.config import settings
from app.rag.ingestion_pipeline.embedder import embedder

collection_name = "pdf_collection"


# QDRANT CLIENT
# Yeh sirf Qdrant se connection banata hai. Koi collection yahan nahi banti.
QClient = QdrantClient(
    api_key=settings.QDRANT_API_KEY,
    url=settings.QDRANT_URL,
)


def create_collection_if_missing() -> None:
    if not QClient.collection_exists(collection_name=collection_name):
        QClient.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(
                size=384,  # MiniLM ke 384 numbers ke hisaab se
                distance=Distance.COSINE,  # closeness COSINE se naapenge
            ),
        )


def collection_exists() -> bool:
    # Sirf collection ka hona check karo.
    # Hum upload pe 0-chunk wali file rok dete hain, isliye "collection hai" ka
    # matlab hamesha "usme chunks bhi hain". points_count check ki zaroorat nahi.
    return QClient.collection_exists(collection_name=collection_name)


# QDRANT VECTOR STORE
# validate_collection_config=False -> import pe collection exist na ho to bhi crash na ho.
# Collection ensure karna ab humara kaam hai (ensure_collection se), iska nahi.
QVectorDb = QdrantVectorStore(
    client=QClient,
    collection_name=collection_name,
    embedding=embedder,
    validate_collection_config=False,
)
