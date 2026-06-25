from fastapi import APIRouter, HTTPException
from qdrant_client.models import Distance, VectorParams
from app.vector_db.qdrant_vector_db import QClient, QVectorDb, collection_name
from app.rag.ingestion_pipeline.ingestion import get_pdf_chunks

rag_router = APIRouter(
    prefix="/rag",
    tags=["rag"],
)


@rag_router.post("/ingest")
async def ingest_pdf():

    try:
        collection_exists = QClient.collection_exists(collection_name=collection_name)

        if not collection_exists:
            QClient.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(
                    size=384,
                    distance=Distance.COSINE,
                ),
            )
        else:
            data = QClient.get_collection(collection_name=collection_name)
            if data.points_count > 0:
                return {
                    "status": "skipped",
                    "detail": "Document already exists",
                }

        chunks = await get_pdf_chunks()

        await QVectorDb.aadd_documents(documents=chunks)

        return {
            "status": "success",
            "detail": "PDF ingested successfully",
        }

    except FileNotFoundError as fnf:
        raise HTTPException(status_code=404, detail=str(fnf))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
