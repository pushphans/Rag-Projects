from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
import io
from pypdf import PdfReader


async def get_pdf_chunks_from_bytes(pdf_file: bytes, source: str) -> list[Document]:

    memory_file = io.BytesIO(pdf_file)

    reader = PdfReader(memory_file)

    docs = []

    for page_number, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            document = Document(
                page_content=text,
                metadata={
                    "page_number": page_number + 1,
                    "source": source,
                },
            )
            docs.append(document)

    # SPLITTER OBJECT
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=400,
        chunk_overlap=80,
    )

    chunks_docs = splitter.split_documents(documents=docs)

    return chunks_docs
