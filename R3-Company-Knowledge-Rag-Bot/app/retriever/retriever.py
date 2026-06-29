from app.vector_db.qdrant import qdrant_db


async def search_chunks(query: str, k=5):
    chunks = await qdrant_db.similarity_search(
        k=k,
        query=query,
    )

    return chunks
