from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import Document
from app.schemas.document import DocumentCreate, DocumentResponse
from app.schemas.pagination import PaginatedResponse
from app.services.pagination import build_paginated_response


router = APIRouter(prefix="/documents", tags=["documents"])

@router.post("/", response_model=DocumentResponse)
def create_document(document: DocumentCreate, db: Session = Depends(get_db)):
    new_document = Document(filename=document.filename, file_type=document.file_type)
    db.add(new_document)
    db.commit()
    db.refresh(new_document)
    return new_document

@router.get("/", response_model=PaginatedResponse[DocumentResponse])
def list_documents(
    offset: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    q: str | None = Query(None, min_length=1)
):

    query = db.query(Document)
    if q is not None:
        search_pattern = f"%{q}%"
        query = query.filter(Document.filename.ilike(search_pattern))
    query = query.order_by(
            Document.created_at.desc(),
            Document.id.desc(),
        )
    return build_paginated_response(query, limit, offset)

@router.get("/{document_id}", response_model=DocumentResponse)
def get_document(document_id: int, db: Session = Depends(get_db)):
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return document