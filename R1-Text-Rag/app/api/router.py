from fastapi import APIRouter, HTTPException
from langchain.messages import HumanMessage
from pydantic import BaseModel
from app.rag.retreival_workflow.rag_state import RagState
from app.rag.vector_db import vector_db
from app.rag.splitter import chunked_docs
from app.rag.retreival_workflow.rag_graph import rag_workflow



rag_router = APIRouter(prefix="/rag", tags=["rag"])


# Request Body Schema for User Queries
class QueryRequest(BaseModel):
    question: str

@rag_router.post("/ingest")
async def ingest_data():
    try:
        vector_db.add_documents(chunked_docs)

        return {"message": "Data ingested successfully."}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error ingesting data: {str(e)}")
    



@rag_router.post("/query")
async def query_data(query_request: QueryRequest):
    try:
        init_state : RagState = {
            "messages" : [HumanMessage(content=query_request.question)],
            "retrieved_docs" : []
        }

        final_state : RagState = await rag_workflow.ainvoke(init_state)

        return {
            "answer" : final_state["messages"][-1].content
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")