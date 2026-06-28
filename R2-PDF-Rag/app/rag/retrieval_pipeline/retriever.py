from app.vector_db.qdrant_vector_db import QVectorDb


async def search_chunks(query: str, k: int = 3) -> list:

    result = await QVectorDb.asimilarity_search(query=query, k=k)
    return result
