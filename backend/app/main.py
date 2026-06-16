from fastapi import FastAPI
from app.api import health, documents, chunks, upload, claims, verification

app = FastAPI()
app.include_router(health.router)
app.include_router(documents.router)
app.include_router(chunks.router)
app.include_router(upload.router)
app.include_router(claims.router)
app.include_router(verification.router)