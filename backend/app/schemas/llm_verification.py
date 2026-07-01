from pydantic import BaseModel, Field
from app.schemas.verification import VerificationStatus

class LLMEvidenceCandidate(BaseModel):
    chunk_id: int
    document_id: int
    filename: str
    page_number: int | None
    chunk_index: int
    content: str
    score: float

class LLMVerificationInput(BaseModel):
    claim_text: str
    source_text: str | None = None
    evidence_candidates: list[LLMEvidenceCandidate]

class LLMVerificationOutput(BaseModel):
    status: VerificationStatus
    confidence: float = Field(ge=0, le=1)
    reasoning: str = Field(min_length=1)
    evidence_chunk_id: int | None = None