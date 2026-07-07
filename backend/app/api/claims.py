from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import (
    Claim, 
    VerificationResult,
    DocumentChunk,
    )
from app.schemas.claim import (
    ClaimCreate, 
    ClaimResponse, 
    )
from app.schemas.evidence import EvidenceResponse
from app.schemas.verification import (
    ClaimVerificationRequest,
    VerificationMode,
    VerificationResultResponse
    )
from app.schemas.pagination import PaginatedResponse
from app.schemas.llm_verification import (
    LLMEvidenceCandidate, 
    LLMVerificationInput, 
    )
from app.services.retrieval import retrieve_evidence_for_claim
from app.services.verification import generate_rule_based_verification
from app.services.pagination import build_paginated_response
from app.services.llm_verification import(
    OpenAIVerificationProvider,
    RuleBasedFallbackProvider,
    )
from sqlalchemy import or_


router = APIRouter(prefix="/claims", tags=["claims"])

def build_llm_evidence_candidates(
        evidences: list[EvidenceResponse],
        db: Session
) -> list[LLMEvidenceCandidate]:
    candidates = []

    for evidence in evidences:
        chunk = (
            db.query(DocumentChunk)
            .filter(DocumentChunk.id == evidence.chunk_id)
            .first()
        )

        if chunk is None:
            raise HTTPException(status_code = 404, detail = "Chunk not found")
        candidates.append(
            LLMEvidenceCandidate(
                chunk_id=evidence.chunk_id,
                document_id=evidence.document_id,
                filename=chunk.document.filename,
                page_number=evidence.page_number,
                chunk_index=evidence.chunk_index,
                content=evidence.content,
                score=evidence.score,
            )
        )

    return candidates


@router.post("/", response_model=ClaimResponse)
def create_claim(claim: ClaimCreate, db: Session = Depends(get_db)):
    new_claim = Claim(claim_text=claim.claim_text, source_text=claim.source_text)
    db.add(new_claim)
    db.commit()
    db.refresh(new_claim)
    return new_claim

@router.post("/{claim_id}/verify", response_model=VerificationResultResponse)
def verify_claim(claim_id: int, db: Session = Depends(get_db), verification_request: ClaimVerificationRequest | None = None,):
    claim = db.query(Claim).filter(Claim.id == claim_id).first()
    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found")
    mode = (
        verification_request.mode
        if verification_request is not None
        else VerificationMode.RULE_BASED
    )
    evidences = retrieve_evidence_for_claim(claim, db)
    if mode == VerificationMode.RULE_BASED:
        verification_data = generate_rule_based_verification(evidences)
    elif mode == VerificationMode.OPEN_AI:
        llm_evidence_candidates = build_llm_evidence_candidates(evidences, db)
        llm_input = LLMVerificationInput(
            claim_text = claim.claim_text,
            source_text = claim.source_text,
            evidence_candidates = llm_evidence_candidates
        )
        try:
            openai_provider = OpenAIVerificationProvider()
            llm_output = openai_provider.verify(llm_input)
        except Exception:
            fallback_provider = RuleBasedFallbackProvider()
            llm_output = fallback_provider.verify(llm_input)
       
        verification_data = {
            "evidence_chunk_id": llm_output.evidence_chunk_id,
            "status": llm_output.status.value,
            "confidence": llm_output.confidence,
            "reasoning": llm_output.reasoning,
        }
    else:
        raise HTTPException(
            status_code=400,
            detail="Unsupported verification mode",
        )
        
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
    db: Session = Depends(get_db),
    q: str | None = Query(None, min_length=1),
):
    query = db.query(Claim)

    if q is not None:
        search_pattern = f"%{q}%"
        query = query.filter(
            or_(
                Claim.claim_text.ilike(search_pattern),
                Claim.source_text.ilike(search_pattern),
            )
        )

    query = query.order_by(
        Claim.created_at.desc(),
        Claim.id.desc(),
    )
    return build_paginated_response(query, limit, offset)

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







    