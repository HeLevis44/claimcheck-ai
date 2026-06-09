from fastapi import FastAPI
from app.api import health
from app.api import documents

app = FastAPI()
app.include_router(health.router)
app.include_router(documents.router)