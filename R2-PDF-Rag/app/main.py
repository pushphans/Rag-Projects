from fastapi import FastAPI
from app.api.rag_router import rag_router

app = FastAPI()

app.include_router(router= rag_router)
