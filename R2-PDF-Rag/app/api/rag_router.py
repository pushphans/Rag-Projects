from fastapi import APIRouter, HTTPException, File, UploadFile
from app.vector_db.qdrant_vector_db import (
    QVectorDb,
    QClient,
    collection_name,
    collection_exists,
    create_collection_if_missing,
)
from app.rag.ingestion_pipeline.ingestion import get_pdf_chunks_from_bytes
from app.rag.retrieval_pipeline.retriever import search_chunks

rag_router = APIRouter(
    prefix="/rag",
    tags=["rag"],
)


# FLOW: check() -> false to upload hone do, true to "pehle delete kar".
# Koi try/except nahi. raise HTTPException(...) ko FastAPI khud user tak bhej deta hai.
@rag_router.post("/upload")
async def ingest_pdf(file: UploadFile = File(...)):

    # GUARD 1: PDF hi hona chahiye
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    # GUARD 2: file khaali na ho. bytes pehle hi padh lo, size check karo.
    # Empty file yahin ruk jaegi -> kabhi collection_exists() tak nahi pahunchegi.
    pdf_file = await file.read()
    if len(pdf_file) == 0:
        raise HTTPException(status_code=400, detail="Uploaded file is empty")

    # GUARD 3: pehle se doc hai to dobara upload mat karne do
    if collection_exists():
        raise HTTPException(
            status_code=400,
            detail="Document already exists. Delete it first, then upload.",
        )

    # Collection user ke upload pe banti hai (sirf agar missing ho).
    create_collection_if_missing()

    chunks = await get_pdf_chunks_from_bytes(pdf_file=pdf_file, source=file.filename)

    # GUARD 4: scanned/image PDF -> text nahi nikla -> 0 chunks.
    # Aisi file ki collection mat banao. Yahi guarantee deta hai ki
    # "collection hai" ka matlab hamesha "usme chunks hain".
    if len(chunks) == 0:
        QClient.delete_collection(collection_name=collection_name)
        raise HTTPException(
            status_code=400,
            detail="No text found in the PDF (maybe scanned/image-only).",
        )

    await QVectorDb.aadd_documents(documents=chunks)

    return {
        "status": "success",
        "detail": f"{file.filename} uploaded and ingested successfully",
        "chunks_added": len(chunks),
    }


# FLOW: check() -> true to retrieve karo, false to "pehle ingest kar".
@rag_router.post("/docs")
async def get_docs(query: str):

    if not collection_exists():
        raise HTTPException(
            status_code=400,
            detail="No ingested data found. Please upload a PDF file first.",
        )

    result = await search_chunks(query=query)

    # Document object seedha JSON nahi banta -> plain dict mein badalna padta hai.
    formatted = []
    for doc in result:
        formatted.append(
            {
                "content": doc.page_content,
                "source": doc.metadata.get("source"),
                "page": doc.metadata.get("page_number"),
            }
        )

    return {"results": formatted}


# FLOW: check() -> true to delete kar do, false to "delete karne ko kuch nahi".
@rag_router.delete("/delete")
async def delete_docs():

    if not collection_exists():
        raise HTTPException(
            status_code=400,
            detail="No documents available to delete, upload a document first",
        )

    QClient.delete_collection(collection_name=collection_name)

    return {
        "status": "success",
        "detail": "Successfully deleted the document",
    }
