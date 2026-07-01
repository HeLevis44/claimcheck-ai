import pytest
from pydantic import ValidationError
from app.schemas.llm_verification import (
    LLMEvidenceCandidate,
    LLMVerificationInput,
    LLMVerificationOutput,
)
from app.schemas.verification import VerificationStatus
from app.services.llm_verification import (
    LLMVerificationProvider,
    RuleBasedFallbackProvider,
    )

class FakeLLMVerificationProvider:
    def verify(
        self,
        input_data: LLMVerificationInput,
    ) -> LLMVerificationOutput:
        return LLMVerificationOutput(
            status=VerificationStatus.LIKELY_SUPPORTED,
            confidence=0.9,
            reasoning="The evidence directly supports the claim.",
            evidence_chunk_id=input_data.evidence_candidates[0].chunk_id,
        )

def test_fake_llm_provider_returns_standardized_output():
    evidence_candidate = LLMEvidenceCandidate(
        chunk_id=101,
        document_id=12,
        filename="orion_report.pdf",
        page_number=3,
        chunk_index=0,
        content="Orion completed the Zephyr project in 2025.",
        score=4.0,
    )

    verification_input = LLMVerificationInput(
        claim_text="Orion completed the Zephyr project in 2025.",
        source_text="A project completion claim.",
        evidence_candidates=[evidence_candidate],
    )

    provider: LLMVerificationProvider = FakeLLMVerificationProvider()

    result = provider.verify(verification_input)

    assert result.status == VerificationStatus.LIKELY_SUPPORTED
    assert result.confidence == 0.9
    assert result.reasoning == "The evidence directly supports the claim."
    assert result.evidence_chunk_id == 101

def test_llm_verification_output_validates_required_constraints():
    with pytest.raises(ValidationError):
        LLMVerificationOutput(
            status=VerificationStatus.LIKELY_SUPPORTED,
            confidence=1.1,
            reasoning="The evidence supports the claim.",
            evidence_chunk_id=101,
        )

    with pytest.raises(ValidationError):
        LLMVerificationOutput(
            status=VerificationStatus.LIKELY_SUPPORTED,
            confidence=0.8,
            reasoning="",
            evidence_chunk_id=101,
        )

    result = LLMVerificationOutput(
        status=VerificationStatus.NOT_ENOUGH_EVIDENCE,
        confidence=0.2,
        reasoning="No retrieved evidence directly supports the claim.",
        evidence_chunk_id=None,
    )
    assert result.evidence_chunk_id is None

def test_rule_based_fallback_provider_returns_standardized_output():
    evidence_candidate = LLMEvidenceCandidate(
        chunk_id=201,
        document_id=22,
        filename="zephyr_report.pdf",
        page_number=4,
        chunk_index=1,
        content="Zephyr launched the Orion platform in 2025.",
        score=3.0,
    )

    verification_input = LLMVerificationInput(
        claim_text="Zephyr launched the Orion platform in 2025.",
        source_text=None,
        evidence_candidates=[evidence_candidate],
    )

    provider = RuleBasedFallbackProvider()

    result = provider.verify(verification_input)

    assert result.status == VerificationStatus.LIKELY_SUPPORTED
    assert result.confidence == 0.8
    assert result.evidence_chunk_id == 201
    assert result.reasoning