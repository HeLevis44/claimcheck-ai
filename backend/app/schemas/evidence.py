from pydantic import BaseModel

class EvidenceResponse(BaseModel):
    chunk_id: int
    document_id: int
    page_number: int
    chunk_index: int
    content: str
    score: int