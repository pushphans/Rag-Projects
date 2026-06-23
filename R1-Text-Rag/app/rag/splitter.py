from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.rag.loader import docs


splitter = RecursiveCharacterTextSplitter(
    chunk_size=100,
    chunk_overlap = 10,
)

chunked_docs = splitter.split_documents(docs)

# print(chunked_docs)
