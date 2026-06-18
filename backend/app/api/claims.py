from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import Claim, VerificationResult
from app.schemas.claim import ClaimCreate, ClaimResponse
from app.schemas.evidence import EvidenceResponse
from app.schemas.verification import VerificationResultResponse
from app.services.retrieval import retrieve_evidence_for_claim

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
    if not evidences:
        status = "not_enough_evidence"
        confidence = 0.2
        reasoning = "No relevant evidence chunks were found."
        evidence_chunk_id = None
    else:
        top_evidence = evidences[0]
        evidence_chunk_id = top_evidence.chunk_id
        if top_evidence.score >= 3:
            status = "likely_supported"
            confidence = 0.8
            reasoning = "The top evidence chunk matched multiple claim keywords."
        else:
            status = "weak_evidence"
            confidence = 0.5
            reasoning = "Only limited keyword overlap was found between the claim and evidence."

    new_verification_Result = VerificationResult(
        claim_id = claim.id,
        evidence_chunk_id = evidence_chunk_id,
        status = status,
        confidence = confidence,
        reasoning = reasoning
    )
    db.add(new_verification_Result)
    db.commit()
    db.refresh(new_verification_Result)
    return new_verification_Result
        


@router.get("/", response_model=list[ClaimResponse])
def get_claims(db: Session = Depends(get_db)):
    claims = db.query(Claim).all()
    return claims

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







    