from fastapi import APIRouter, HTTPException, UploadFile
from fastapi.param_functions import File

from app.ingestion.ingester import make_chunks
from app.retriever.retriever import search_chunks
from app.vector_db.qdrant import (
    COLLECTION_NAME,
    client,
    collection_exists,
    create_collection_if_missing,
    qdrant_db,
)

rag_router = APIRouter(prefix="/rag")


# INGEST ENDPOINT
@rag_router.post("/upload")
async def upload_docs(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Uploaded file is not of type .pdf")

    read = await file.read()

    if len(read) == 0:
        raise HTTPException(status_code=400, detail="The content in file is empty")

    create_collection_if_missing()

    chunks = await make_chunks(file=read, source=file.filename)

    if len(chunks) == 0:
        client.delete_collection(
            collection_name=COLLECTION_NAME,
        )

        raise HTTPException(
            status_code=400,
            detail="the uploaded document is empty",
        )

    await qdrant_db.aadd_documents(documents=chunks)

    return {
        "status": "success",
        "detail": f"{file.filename} is added successfully",
        "chunks_add": len(chunks),
    }


# DELETE ENDPOINT
@rag_router.delete("/delete")
async def delete_docs():
    result = collection_exists()

    if not result:
        raise HTTPException(status_code=400, detail="No document to delete")

    client.delete_collection(collection_name=COLLECTION_NAME)

    return {
        "status": "success",
        "detail": "document deleted successfully",
    }


# RETRIEVE ENDPOINT
@rag_router.post("/retrieve")
async def retrieve_chunks(query: str):
    exists = collection_exists()

    if not exists:
        raise HTTPException(status_code=400, detail="No document found")

    result = await search_chunks(query=query)

    return {"results": result}
