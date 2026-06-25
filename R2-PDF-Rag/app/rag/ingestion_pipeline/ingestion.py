from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pathlib import Path

file_path = Path("app/sample_data/sample.pdf").resolve()


async def get_pdf_chunks() -> list[Document]:

    if not file_path.exists():
        raise FileNotFoundError("File not found")

    # LOADER OBJECT
    loader = PyPDFLoader(
        file_path=str(file_path),
    )

    docs = await loader.aload()

    # SPLITTER OBJECT
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=100,
        chunk_overlap=10,
    )

    chunks_docs = splitter.split_documents(documents=docs)

    return chunks_docs
