from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import DocumentChunk, Document
from app.schemas.chunk import ChunkCreate, ChunkResponse


router = APIRouter(prefix="/documents/{document_id}/chunks", tags=["chunks"])

@router.post("/", response_model=ChunkResponse)
def create_chunk(chunk: ChunkCreate, document_id: int, db: Session = Depends(get_db)):
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    new_chunk = DocumentChunk(
        document_id=document_id,
        page_number=chunk.page_number,
        chunk_index=chunk.chunk_index,
        content=chunk.content
    )
    db.add(new_chunk)
    db.commit()
    db.refresh(new_chunk)
    return new_chunk

@router.get("/", response_model=list[ChunkResponse])
def get_chunks(document_id: int, db: Session = Depends(get_db)):
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    chunks = db.query(DocumentChunk).filter(DocumentChunk.document_id == document_id).all()
    return chunks