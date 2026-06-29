import asyncio
from pypdf import PdfReader
from langchain_core.documents import Document
import io
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings


def _parse_pdf_sync(file_bytes: bytes, source: str) -> list[Document]:
    memory_file = io.BytesIO(file_bytes)
    reader = PdfReader(memory_file)

    doc = []

    for page_number, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            document = Document(
                page_content=text,
                metadata={
                    "source": source,
                    page_number: page_number + 1,
                },
            )

            doc.append(document)

    return doc


async def make_chunks(file: bytes, source: str) -> list[Document]:

    # RUN PDF PARSING IN THREAD POOL TO NOT BLOCK EVENT LOOP
    doc = await asyncio.to_thread(_parse_pdf_sync, file, source)

    # MAKE SPLITTER FOR CHUNKING
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=400,
        chunk_overlap=80,
    )

    # SPLIT DCOUMENT INTO CHUNKS
    chunks = splitter.split_documents(documents=doc)

    return chunks


# EMBEDDER INSTANCE FOR EMBEDDINGS
embedder = HuggingFaceEmbeddings(
    model="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={
        "device": "cpu",
    },
)
