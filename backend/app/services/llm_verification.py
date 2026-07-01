from typing import Protocol
from app.services.verification import generate_rule_based_verification
from app.schemas.verification import VerificationStatus
from app.schemas.llm_verification import (
    LLMVerificationInput,
    LLMVerificationOutput,
)

class LLMVerificationProvider(Protocol):
    def verify(self, input_data: LLMVerificationInput) -> LLMVerificationOutput:
        ...

class RuleBasedFallbackProvider:
    def verify(self, input_data: LLMVerificationInput) -> LLMVerificationOutput:
        result = generate_rule_based_verification(input_data.evidence_candidates)

        return LLMVerificationOutput(
            status=VerificationStatus(result["status"]),
            confidence=result["confidence"],
            reasoning=result["reasoning"],
            evidence_chunk_id=result["evidence_chunk_id"],
        )