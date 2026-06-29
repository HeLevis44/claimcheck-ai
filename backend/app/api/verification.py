from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import VerificationResult, Claim, DocumentChunk
from app.schemas.verification import VerificationResultCreate, VerificationResultResponse, VerificationDetailResponse
from app.schemas.pagination import PaginatedResponse
from app.services.verification_detail import build_verification_detail_response

router = APIRouter(prefix="/verification-results", tags=["verification-results"])

@router.post("/", response_model=VerificationResultResponse)
def create_verification_result(verification: VerificationResultCreate, db: Session = Depends(get_db)):
    claim = db.query(Claim).filter(Claim.id == verification.claim_id).first()
    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found")
    
    evidence_chunk_id = None
    if verification.evidence_chunk_id is not None:
        evidence_chunk = db.query(DocumentChunk).filter(DocumentChunk.id == verification.evidence_chunk_id).first()
        if not evidence_chunk:
            raise HTTPException(status_code=404, detail="Evidence chunk not found")
        evidence_chunk_id = evidence_chunk.id
    
    db_verification_result = VerificationResult(
        claim_id=claim.id,
        evidence_chunk_id=evidence_chunk_id,
        status=verification.status,
        confidence=verification.confidence,
        reasoning=verification.reasoning
    )
    db.add(db_verification_result)
    db.commit()
    db.refresh(db_verification_result)
    return db_verification_result

@router.get("/", response_model=PaginatedResponse[VerificationResultResponse])
def get_verification_results(
        limit: int = Query(20, ge=1, le=100),
        offset: int = Query(0, ge=0),
        db: Session = Depends(get_db),
    ):
    total = db.query(VerificationResult).count()
    items = db.query(VerificationResult).order_by(
        VerificationResult.created_at.desc(),
        VerificationResult.id.desc(),
        ).offset(offset).limit(limit).all()
    
    return {
        "items": items,
        "total": total,
        "limit": limit,
        "offset": offset,
        "has_more": offset+len(items)<total
    }

@router.get("/claim/{claim_id}", response_model=list[VerificationResultResponse])
def get_verification_claim(claim_id: int, db: Session = Depends(get_db)):
    claim = db.query(Claim).filter(Claim.id == claim_id).first()
    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found")
    return db.query(VerificationResult).filter(VerificationResult.claim_id == claim_id).all()

@router.get("/{verification_id}/detail",response_model=VerificationDetailResponse)
def get_verification_result_detail(verification_id: int, db: Session = Depends(get_db)):
    verification = db.query(VerificationResult).filter(VerificationResult.id == verification_id).first()
    if not verification:
        raise HTTPException(status_code=404, detail="Verification result not found")
    return build_verification_detail_response(verification)

@router.get("/{verification_id}", response_model=VerificationResultResponse)
def get_verification_result(verification_id: int, db: Session = Depends(get_db)):
    verification_result = db.query(VerificationResult).filter(VerificationResult.id == verification_id).first()
    if not verification_result:
        raise HTTPException(status_code=404, detail="Verification result not found")
    return verification_result
