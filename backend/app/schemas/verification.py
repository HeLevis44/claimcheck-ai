from pydantic import BaseModel, ConfigDict
from datetime import datetime
from enum import Enum

class VerificationStatus(str, Enum):
    LIKELY_SUPPORTED = "likely_supported"
    WEAK_EVIDENCE = "weak_evidence"
    NOT_ENOUGH_EVIDENCE = "not_enough_evidence"

class VerificationResultCreate(BaseModel):
    claim_id: int
    evidence_chunk_id: int | None
    status: VerificationStatus
    confidence: float
    reasoning: str | None

class VerificationResultResponse(BaseModel):
    id: int
    claim_id: int
    evidence_chunk_id: int | None
    status: VerificationStatus
    confidence: float
    reasoning: str | None
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class ClaimSummaryResponse(BaseModel):
    id: int
    claim_text: str
    source_text: str | None
    model_config = ConfigDict(from_attributes=True)

class EvidenceDetailResponse(BaseModel):
    id: int
    document_id: int
    filename: str
    page_number: int
    chunk_index: int
    content: str
    model_config = ConfigDict(from_attributes=True)

class VerificationSummaryResponse(BaseModel):
    id: int
    status: VerificationStatus
    confidence: float
    reasoning: str | None
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class VerificationDetailResponse(BaseModel):
    verification: VerificationSummaryResponse
    claim: ClaimSummaryResponse
    evidence: EvidenceDetailResponse | None

