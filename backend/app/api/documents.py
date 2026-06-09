from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import Document
from app.schemas.document import DocumentCreate, DocumentResponse


router = APIRouter(prefix="/documents", tags=["documents"])

@router.post("/", response_model=DocumentResponse)
def create_document(document: DocumentCreate, db: Session = Depends(get_db)):
    new_document = Document(filename=document.filename, file_type=document.file_type)
    db.add(new_document)
    db.commit()
    db.refresh(new_document)
    return new_document

@router.get("/", response_model=list[DocumentResponse])
def list_documents(db: Session = Depends(get_db)):
    documents = db.query(Document).all()
    return documents

@router.get("/{document_id}", response_model=DocumentResponse)
def get_document(document_id: int, db: Session = Depends(get_db)):
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return document