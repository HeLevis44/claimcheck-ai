from fastapi import APIRouter
from sqlalchemy import text
from app.db.database import SessionLocal

router = APIRouter()

@router.get("/health")
def health_check():
    return {"status": "healthy"}

@router.get("/health/db")
def db_health_check():
    db = SessionLocal()
    try:
        db.execute(text("SELECT 1"))
        return {"status": "healthy"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}
    finally:
        db.close()