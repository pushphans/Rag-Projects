from fastapi import FastAPI, APIRouter
from app.api.router import rag_router


app = FastAPI()
app.include_router(rag_router)