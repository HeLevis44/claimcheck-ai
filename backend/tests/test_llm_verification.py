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
    OpenAIVerificationProvider,
    RuleBasedFallbackProvider,
)
from unittest.mock import patch

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

def test_openai_provider_uses_provided_client_and_model():
    fake_client = object()

    provider = OpenAIVerificationProvider(
        client=fake_client,
        model="gpt-4.1-mini",
    )

    assert provider.client is fake_client
    assert provider.model == "gpt-4.1-mini"

def test_openai_provider_creates_default_client_when_none_is_provided():
    fake_default_client = object()

    with patch(
        "app.services.llm_verification.OpenAI",
        return_value=fake_default_client,
    ):
        provider = OpenAIVerificationProvider()

    assert provider.client is fake_default_client
    assert provider.model == "gpt-4.1-mini"

def test_openai_provider_builds_prompt():
    evidence_candidate = LLMEvidenceCandidate(
        chunk_id=301,
        document_id=30,
        filename="orion_report.pdf",
        page_number=2,
        chunk_index=0,
        content="Orion completed the Zephyr project in 2025.",
        score=4.0,
    )

    verification_input = LLMVerificationInput(
        claim_text="Orion completed the Zephyr project in 2025.",
        source_text="A project completion claim.",
        evidence_candidates=[evidence_candidate],
    )

    provider = OpenAIVerificationProvider(
        client=object(),
        model="gpt-4.1-mini",
    )

    prompt = provider._build_prompt(verification_input)

    assert "You are a claim verification assistant." in prompt
    assert "Verify whether the claim below is supported by the provided evidence." in prompt
    assert "Orion completed the Zephyr project in 2025." in prompt
    assert "A project completion claim." in prompt
    assert '"chunk_id": 301' in prompt
    assert "orion_report.pdf" in prompt
    assert '"likely_supported"' in prompt
    assert '"weak_evidence"' in prompt
    assert '"not_enough_evidence"' in prompt
    assert '"document_id"' not in prompt
    assert '"score"' not in prompt

def test_openai_provider_calls_parse_and_returns_parsed_output():
    evidence_candidate = LLMEvidenceCandidate(
        chunk_id=401,
        document_id=40,
        filename="zephyr_report.pdf",
        page_number=5,
        chunk_index=0,
        content="Zephyr released the Orion report in 2025.",
        score=4.0,
    )

    verification_input = LLMVerificationInput(
        claim_text="Zephyr released the Orion report in 2025.",
        source_text="A report release claim.",
        evidence_candidates=[evidence_candidate],
    )

    expected_output = LLMVerificationOutput(
        status=VerificationStatus.LIKELY_SUPPORTED,
        confidence=0.9,
        reasoning="The evidence directly states that Zephyr released the Orion report in 2025.",
        evidence_chunk_id=401,
    )

    class FakeResponse:
        output_parsed = expected_output

    class FakeResponses:
        def __init__(self):
            self.called_with = None

        def parse(self, **kwargs):
            self.called_with = kwargs
            return FakeResponse()

    class FakeClient:
        def __init__(self):
            self.responses = FakeResponses()

    fake_client = FakeClient()

    provider = OpenAIVerificationProvider(
        client=fake_client,
        model="gpt-4.1-mini",
    )

    result = provider.verify(verification_input)

    assert result == expected_output
    assert fake_client.responses.called_with["model"] == "gpt-4.1-mini"
    assert fake_client.responses.called_with["text_format"] is LLMVerificationOutput
    assert "Zephyr released the Orion report in 2025." in fake_client.responses.called_with["input"]

def test_openai_provider_allows_none_evidence_chunk_id():
    verification_input = LLMVerificationInput(
        claim_text="Orion completed the Zephyr project in 2025.",
        source_text=None,
        evidence_candidates=[],
    )

    expected_output = LLMVerificationOutput(
        status=VerificationStatus.NOT_ENOUGH_EVIDENCE,
        confidence=0.2,
        reasoning="No provided evidence sufficiently supports the claim.",
        evidence_chunk_id=None,
    )

    class FakeResponse:
        output_parsed = expected_output

    class FakeResponses:
        def parse(self, **kwargs):
            return FakeResponse()

    class FakeClient:
        def __init__(self):
            self.responses = FakeResponses()

    provider = OpenAIVerificationProvider(
        client=FakeClient(),
        model="gpt-4.1-mini",
    )

    result = provider.verify(verification_input)

    assert result == expected_output

def test_openai_provider_rejects_unknown_evidence_chunk_id():
    evidence_candidate = LLMEvidenceCandidate(
        chunk_id=501,
        document_id=50,
        filename="orion_report.pdf",
        page_number=1,
        chunk_index=0,
        content="Orion completed the Zephyr project in 2025.",
        score=4.0,
    )

    verification_input = LLMVerificationInput(
        claim_text="Orion completed the Zephyr project in 2025.",
        source_text=None,
        evidence_candidates=[evidence_candidate],
    )

    invalid_output = LLMVerificationOutput(
        status=VerificationStatus.LIKELY_SUPPORTED,
        confidence=0.9,
        reasoning="The evidence supports the claim.",
        evidence_chunk_id=999,
    )

    class FakeResponse:
        output_parsed = invalid_output

    class FakeResponses:
        def parse(self, **kwargs):
            return FakeResponse()

    class FakeClient:
        def __init__(self):
            self.responses = FakeResponses()

    provider = OpenAIVerificationProvider(
        client=FakeClient(),
        model="gpt-4.1-mini",
    )

    with pytest.raises(ValueError, match="Invalid evidence_chunk_id"):
        provider.verify(verification_input)