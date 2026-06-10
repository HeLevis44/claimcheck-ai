from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db.models import Document, DocumentChunk
from app.db.database import get_db
import fitz

def split_text_into_chunks(text, max_chunk_size=400, overlap=50):
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = min(start + max_chunk_size, len(words))
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += max_chunk_size - overlap
    return chunks

router = APIRouter(prefix="/upload", tags=["upload"])

@router.post("/pdf")
def upload_pdf(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF files are allowed.")
    
    new_document = Document(filename=file.filename, file_type=file.content_type)
    db.add(new_document)
    db.commit()
    db.refresh(new_document)

    pdf_bytes = file.file.read()
    pdf = fitz.open(stream=pdf_bytes, filetype="pdf")

    chunk_index = 0
    for page_index in range(pdf.page_count):
        page = pdf.load_page(page_index)
        text = page.get_text()
        chunks = split_text_into_chunks(text)
        if chunks:
            for chunk in chunks:
                new_document_chunk = DocumentChunk(
                    document_id=new_document.id,
                    page_number=page_index + 1,
                    chunk_index=chunk_index,
                    content=chunk
                )
                chunk_index += 1
                db.add(new_document_chunk)
    db.commit()

    return {
        "document_id": new_document.id,
        "filename": new_document.filename,
        "page_count":pdf.page_count,
        "chunk_count": chunk_index
    }
    

    