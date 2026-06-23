from langchain_huggingface import HuggingFaceEmbeddings
from app.rag.splitter import chunked_docs

embedder = HuggingFaceEmbeddings(
    model_name = "sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={
        "device": "cpu"
    }
)

list_of_chunks = []

for chunk in chunked_docs:
    list_of_chunks.append(chunk.page_content)


embeddings = embedder.embed_documents(list_of_chunks)

# print(embeddings)