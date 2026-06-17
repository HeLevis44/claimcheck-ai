from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import re
from app.db.database import get_db
from app.db.models import Claim, DocumentChunk
from app.schemas.claim import ClaimCreate, ClaimResponse
from app.schemas.evidence import EvidenceResponse

router = APIRouter(prefix="/claims", tags=["claims"])

STOP_WORDS = {
    "the", "and", "for", "with", "that", "this", "are", "was", "were",
    "from", "into", "has", "have", "had", "not", "but", "about",
    "than", "then", "they", "their", "there", "which", "when", "where",
    "what", "who", "why", "how", "can", "may", "might", "will",
    "would", "could", "should", "a", "an", "of", "to", "in", "on", "by", "is", "it", "as", "at", "or"
}


def extract_keywords(text: str) -> list[str]:
    cleaned_text = re.sub(r"[^a-zA-Z0-9\s]", " ", text.lower())
    words = cleaned_text.split()
    return [word for word in words if len(word) >= 3 and word not in STOP_WORDS]


@router.post("/", response_model=ClaimResponse)
def create_claim(claim: ClaimCreate, db: Session = Depends(get_db)):
    new_claim = Claim(claim_text=claim.claim_text, source_text=claim.source_text)
    db.add(new_claim)
    db.commit()
    db.refresh(new_claim)
    return new_claim

@router.get("/", response_model=list[ClaimResponse])
def get_claims(db: Session = Depends(get_db)):
    claims = db.query(Claim).all()
    return claims

@router.get("/{claim_id}/evidence", response_model=list[EvidenceResponse])
def get_claim_evidence(claim_id: int, db: Session = Depends(get_db)):
    claim = db.query(Claim).filter(Claim.id == claim_id).first()
    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found")
    
    key_words = extract_keywords(claim.claim_text)
    if not key_words:
        return []

    evidence_list = []
    chunk_scores = {}

    for keyword in key_words:
        chunks = db.query(DocumentChunk).filter(DocumentChunk.content.ilike(f"%{keyword}%")).all()
        for chunk in chunks:
            if chunk.id not in chunk_scores:
                chunk_scores[chunk.id] = {
                    "chunk": chunk,
                    "score": 0
                }
            chunk_scores[chunk.id]["score"] += 1
    sorted_chunks = sorted(chunk_scores.values(), key=lambda x: x["score"], reverse=True)
    for chunk_info in sorted_chunks[:10]:
        chunk = chunk_info["chunk"]
        evidence_list.append(EvidenceResponse(
        chunk_id=chunk.id,
        document_id=chunk.document_id,
        page_number=chunk.page_number,
        chunk_index=chunk.chunk_index,
        content=chunk.content,
        score=chunk_info["score"]
    ))
    return evidence_list

@router.get("/{claim_id}", response_model=ClaimResponse)
def get_claim(claim_id: int, db: Session = Depends(get_db)):
    claim = db.query(Claim).filter(Claim.id == claim_id).first()
    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found")
    return claim







    