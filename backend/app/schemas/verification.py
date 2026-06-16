from pydantic import BaseModel, ConfigDict
from datetime import datetime

class VerificationResultCreate(BaseModel):
    claim_id: int
    evidence_chunk_id: int | None
    status: str
    confidence: float
    reasoning: str | None

class VerificationResultResponse(BaseModel):
    id: int
    claim_id: int
    evidence_chunk_id: int | None
    status: str
    confidence: float
    reasoning: str | None
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)