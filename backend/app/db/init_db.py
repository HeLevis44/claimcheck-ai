from app.db.models import Document, DocumentChunk, Claim, VerificationResult
from app.db.database import engine, Base

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")