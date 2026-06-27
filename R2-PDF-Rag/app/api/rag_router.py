from fastapi import APIRouter, HTTPException, File, UploadFile
from qdrant_client.models import Distance, VectorParams
from app.vector_db.qdrant_vector_db import QVectorDb
from app.rag.ingestion_pipeline.ingestion import get_pdf_chunks_from_bytes

rag_router = APIRouter(
    prefix="/rag",
    tags=["rag"],
)


@rag_router.post("/upload")
async def ingest_pdf(file: UploadFile = File(...)):

    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    try:
        pdf_file = await file.read()

        chunks = await get_pdf_chunks_from_bytes(pdf_file=pdf_file)

        await QVectorDb.aadd_documents(documents=chunks)
        return {
            "status": "success",
            "detail": "PDF file is uploaded and ingested succssfully",
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
