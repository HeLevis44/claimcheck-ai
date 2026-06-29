from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import Claim, VerificationResult
from app.schemas.claim import ClaimCreate, ClaimResponse
from app.schemas.evidence import EvidenceResponse
from app.schemas.verification import VerificationResultResponse
from app.schemas.pagination import PaginatedResponse
from app.services.retrieval import retrieve_evidence_for_claim
from app.services.verification import generate_rule_based_verification


router = APIRouter(prefix="/claims", tags=["claims"])

@router.post("/", response_model=ClaimResponse)
def create_claim(claim: ClaimCreate, db: Session = Depends(get_db)):
    new_claim = Claim(claim_text=claim.claim_text, source_text=claim.source_text)
    db.add(new_claim)
    db.commit()
    db.refresh(new_claim)
    return new_claim

@router.post("/{claim_id}/verify", response_model=VerificationResultResponse)
def verify_claim(claim_id: int, db: Session = Depends(get_db)):
    claim = db.query(Claim).filter(Claim.id == claim_id).first()
    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found")
    evidences = retrieve_evidence_for_claim(claim, db)
    verification_data = generate_rule_based_verification(evidences)

    new_verification_result = VerificationResult(
        claim_id = claim.id,
        evidence_chunk_id = verification_data["evidence_chunk_id"],
        status = verification_data["status"],
        confidence = verification_data["confidence"],
        reasoning = verification_data["reasoning"]
    )
    db.add(new_verification_result)
    db.commit()
    db.refresh(new_verification_result)
    return new_verification_result

@router.get("/", response_model=PaginatedResponse[ClaimResponse])
def get_claims(
    offset: int = Query(0, ge = 0),
    limit: int = Query(20, ge = 1, le = 100),
    db: Session = Depends(get_db)
    ):
    total = db.query(Claim).count()

    items = db.query(Claim).order_by(
        Claim.created_at.desc(),
        Claim.id.desc()
        ).offset(offset).limit(limit).all()

    return {
        "items": items,
        "total": total,
        "limit": limit,
        "offset": offset,
        "has_more": offset+len(items)<total
    }

@router.get("/{claim_id}/evidence", response_model=list[EvidenceResponse])
def get_claim_evidence(claim_id: int, db: Session = Depends(get_db)):
    claim = db.query(Claim).filter(Claim.id == claim_id).first()
    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found")
    return retrieve_evidence_for_claim(claim, db)
    
    

@router.get("/{claim_id}", response_model=ClaimResponse)
def get_claim(claim_id: int, db: Session = Depends(get_db)):
    claim = db.query(Claim).filter(Claim.id == claim_id).first()
    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found")
    return claim







    