from datetime import datetime
from pydantic import BaseModel, ConfigDict

class ClaimCreate(BaseModel):
    claim_text:str
    source_text:str

class ClaimResponse(BaseModel):
    id: int
    claim_text:str
    source_text:str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)