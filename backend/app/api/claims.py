from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import Claim
from app.schemas.claim import ClaimCreate, ClaimResponse

router = APIRouter(prefix="/claims", tags=["claims"])

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

@router.get("/{claim_id}", response_model=ClaimResponse)
def get_claim(claim_id: int, db: Session = Depends(get_db)):
    claim = db.query(Claim).filter(Claim.id == claim_id).first()
    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found")
    return claim