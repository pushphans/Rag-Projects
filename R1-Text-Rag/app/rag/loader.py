from langchain_core.documents import Document
from pathlib import Path


file_path = Path("app/data/sample.txt").resolve()

with open(file_path, "r", encoding="utf-8") as file:
    content = file.read()

docs = [Document(
    page_content=content,
    metadata = {
        "source" : file_path.name, "format" : "text"
    }
)]

# print(docs)