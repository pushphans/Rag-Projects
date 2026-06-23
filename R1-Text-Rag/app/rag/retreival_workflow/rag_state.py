from typing import TypedDict, Annotated
from langchain.messages import AnyMessage
from langgraph.graph.message import add_messages
from langchain_core.documents import Document

class RagState(TypedDict):
    messages : Annotated[list[AnyMessage], add_messages]
    retrieved_docs : list[Document]