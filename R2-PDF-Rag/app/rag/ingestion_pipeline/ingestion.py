from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pathlib import Path
import io
from pypdf import PdfReader


async def get_pdf_chunks_from_bytes(pdf_file: bytes) -> list[Document]:

    memory_file = io.BytesIO(pdf_file)

    reader = PdfReader(memory_file)

    docs = []

    for page_number, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            document = Document(
                page_content=text,
                metadata={"page_number": page_number + 1},
            )
            docs.append(document)

    # SPLITTER OBJECT
    # chunk_size=800 chars (~200 tokens) -> stays within MiniLM's ~256 token limit
    # chunk_overlap=120 (~15% of chunk_size) -> keeps ideas safe across chunk borders
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=120,
    )

    chunks_docs = splitter.split_documents(documents=docs)

    return chunks_docs
