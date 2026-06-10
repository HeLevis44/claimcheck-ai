from fastapi import FastAPI
from app.api import health, documents, chunks

app = FastAPI()
app.include_router(health.router)
app.include_router(documents.router)
app.include_router(chunks.router)