from fastapi.testclient import TestClient
from app.schemas.llm_verification import LLMVerificationOutput
from app.schemas.verification import VerificationStatus
from app.main import app

client = TestClient(app)

def create_test_claim():
    payload = {
    "claim_text": "Glucose enters the TCA cycle through pyruvate.",
    "source_text": "Test source text."
    }

    response = client.post("/claims/", json=payload)

    assert response.status_code == 200
    assert response.json()["claim_text"] == payload["claim_text"]
    assert response.json()["source_text"] == payload["source_text"]
    assert "id" in response.json()
    return response.json()

def test_claims_check():
    create_test_claim()

def test_claims_id_check():
    created_claim = create_test_claim()
    claim_id = created_claim["id"]
    response = client.get(f"/claims/{claim_id}")

    assert response.status_code == 200
    assert response.json()["id"] == claim_id
    assert response.json()["claim_text"] == created_claim["claim_text"]
    assert response.json()["source_text"] == created_claim["source_text"]

def test_404_check():
    response = client.get("/claims/999999")
    assert response.status_code == 404
    assert response.json()["error"]["message"] == "Claim not found"

def test_get_claims_list():
    created_claim = create_test_claim()
    response = client.get("/claims/")

    assert response.status_code == 200


    result = response.json()
    assert isinstance(result, dict)
    assert "items" in result
    assert "total" in result
    assert "limit" in result
    assert "offset" in result
    assert "has_more" in result

    claim_ids = [claim["id"] for claim in result["items"]]
    assert created_claim["id"] in claim_ids

def test_create_claim_missing_required_field():
    payload = {
        "source_text": "Test source text."
    }
    response = client.post("/claims/", json=payload)
    assert response.status_code == 422

def test_get_claims_respects_limit():
    for index in range(3):
        payload = {
            "claim_text": f"Limit pagination claim {index}",
            "source_text": "Pagination test source.",
        }

        create_response = client.post("/claims/", json=payload)
        assert create_response.status_code == 200

    response = client.get("/claims/?limit=2")

    assert response.status_code == 200

    result = response.json()
    assert isinstance(result, dict)
    assert result["total"] == 3
    assert result["limit"] == 2
    assert result["offset"] == 0
    assert len(result["items"]) == 2
    assert result["has_more"] is True

def test_get_claims_respects_offset():
    created_claim_ids = []

    for index in range(3):
        payload = {
            "claim_text": f"Offset pagination claim {index}",
            "source_text": "Pagination test source.",
        }

        create_response = client.post("/claims/", json=payload)
        assert create_response.status_code == 200

        created_claim_ids.append(create_response.json()["id"])

    response = client.get("/claims/?limit=2&offset=1")

    assert response.status_code == 200

    result = response.json()
    assert isinstance(result, dict)
    assert result["total"] == 3
    assert result["limit"] == 2
    assert result["offset"] == 1
    assert len(result["items"]) == 2
    assert result["has_more"] is False

    returned_claim_ids = [claim["id"] for claim in result["items"]]

    assert created_claim_ids[-1] not in returned_claim_ids

def test_get_claims_rejects_zero_limit():
    response = client.get("/claims/?limit=0")

    assert response.status_code == 422

def test_get_claims_rejects_negative_offset():
    response = client.get("/claims/?offset=-1")

    assert response.status_code == 422

def test_get_claims_searches_claim_text():
    matching_payload = {
        "claim_text": "Orion protocol is active",
        "source_text": "General source text.",
    }
    non_matching_payload = {
        "claim_text": "Unrelated statement",
        "source_text": "Another source text.",
    }

    matching_response = client.post("/claims/", json=matching_payload)
    assert matching_response.status_code == 200

    non_matching_response = client.post("/claims/", json=non_matching_payload)
    assert non_matching_response.status_code == 200

    response = client.get("/claims/?q=orion")

    assert response.status_code == 200

    result = response.json()
    assert result["total"] == 1
    assert len(result["items"]) == 1
    assert result["items"][0]["id"] == matching_response.json()["id"]

def test_get_claims_searches_source_text_case_insensitively():
    matching_payload = {
        "claim_text": "A neutral claim",
        "source_text": "Contains ZEPHYR reference.",
    }
    non_matching_payload = {
        "claim_text": "Another neutral claim",
        "source_text": "Different source.",
    }

    matching_response = client.post("/claims/", json=matching_payload)
    assert matching_response.status_code == 200

    non_matching_response = client.post("/claims/", json=non_matching_payload)
    assert non_matching_response.status_code == 200

    response = client.get("/claims/?q=zephyr")

    assert response.status_code == 200

    result = response.json()
    assert result["total"] == 1
    assert len(result["items"]) == 1
    assert result["items"][0]["id"] == matching_response.json()["id"]

def test_get_claims_search_returns_empty_result_when_no_match():
    payload = {
        "claim_text": "A neutral claim",
        "source_text": "A neutral source.",
    }

    create_response = client.post("/claims/", json=payload)
    assert create_response.status_code == 200

    response = client.get("/claims/?q=nonexistentkeyword")

    assert response.status_code == 200

    result = response.json()
    assert result["items"] == []
    assert result["total"] == 0
    assert result["has_more"] is False

def test_verify_claim_defaults_to_rule_based_when_body_is_omitted():
    claim_response = client.post(
        "/claims/",
        json={
            "claim_text": "Orion completed the Zephyr project in 2025.",
            "source_text": "A project completion claim.",
        },
    )
    assert claim_response.status_code == 200

    claim_id = claim_response.json()["id"]

    response = client.post(f"/claims/{claim_id}/verify")

    assert response.status_code == 200
    result = response.json()
    assert result["status"] == "not_enough_evidence"
    assert result["evidence_chunk_id"] is None

def test_verify_claim_uses_openai_provider_when_mode_is_openai(monkeypatch):
    class FakeOpenAIVerificationProvider:
        last_input = None

        def verify(self, input_data):
            FakeOpenAIVerificationProvider.last_input = input_data

            return LLMVerificationOutput(
                status=VerificationStatus.NOT_ENOUGH_EVIDENCE,
                confidence=0.2,
                reasoning="No provided evidence sufficiently supports the claim.",
                evidence_chunk_id=None,
            )

    monkeypatch.setattr(
        "app.api.claims.OpenAIVerificationProvider",
        FakeOpenAIVerificationProvider,
    )

    claim_response = client.post(
        "/claims/",
        json={
            "claim_text": "Orion completed the Zephyr project in 2025.",
            "source_text": "A project completion claim.",
        },
    )
    assert claim_response.status_code == 200

    claim_id = claim_response.json()["id"]

    response = client.post(
        f"/claims/{claim_id}/verify",
        json={"mode": "openai"},
    )

    assert response.status_code == 200

    result = response.json()
    assert result["status"] == "not_enough_evidence"
    assert result["confidence"] == 0.2
    assert result["evidence_chunk_id"] is None

    assert FakeOpenAIVerificationProvider.last_input is not None
    assert (
        FakeOpenAIVerificationProvider.last_input.claim_text
        == "Orion completed the Zephyr project in 2025."
    )
    assert (
        FakeOpenAIVerificationProvider.last_input.source_text
        == "A project completion claim."
    )
    assert FakeOpenAIVerificationProvider.last_input.evidence_candidates == []

def test_verify_claim_rejects_invalid_mode():
    claim_response = client.post(
        "/claims/",
        json={
            "claim_text": "Orion completed the Zephyr project in 2025.",
            "source_text": "A project completion claim.",
        },
    )
    assert claim_response.status_code == 200

    claim_id = claim_response.json()["id"]

    response = client.post(
        f"/claims/{claim_id}/verify",
        json={"mode": "unknown"},
    )

    assert response.status_code == 422

    result = response.json()
    assert result["error"]["code"] == "validation_error"
    assert result["error"]["message"] == "Request validation failed"
    assert isinstance(result["error"]["fields"], list)
    assert result["error"]["fields"]

def test_verify_claim_falls_back_to_rule_based_when_openai_provider_fails(
    monkeypatch,
):
    from app.schemas.llm_verification import LLMVerificationOutput
    from app.schemas.verification import VerificationStatus

    class FailingOpenAIVerificationProvider:
        def __init__(self):
            raise RuntimeError("OpenAI provider is unavailable")

    class FakeRuleBasedFallbackProvider:
        last_input = None

        def verify(self, input_data):
            FakeRuleBasedFallbackProvider.last_input = input_data

            return LLMVerificationOutput(
                status=VerificationStatus.NOT_ENOUGH_EVIDENCE,
                confidence=0.2,
                reasoning="Fallback verification result.",
                evidence_chunk_id=None,
            )

    monkeypatch.setattr(
        "app.api.claims.OpenAIVerificationProvider",
        FailingOpenAIVerificationProvider,
    )
    monkeypatch.setattr(
        "app.api.claims.RuleBasedFallbackProvider",
        FakeRuleBasedFallbackProvider,
    )

    claim_response = client.post(
        "/claims/",
        json={
            "claim_text": "Orion completed the Zephyr project in 2025.",
            "source_text": "A project completion claim.",
        },
    )
    assert claim_response.status_code == 200

    claim_id = claim_response.json()["id"]

    response = client.post(
        f"/claims/{claim_id}/verify",
        json={"mode": "openai"},
    )

    assert response.status_code == 200

    result = response.json()
    assert result["status"] == "not_enough_evidence"
    assert result["confidence"] == 0.2
    assert result["reasoning"] == "Fallback verification result."
    assert result["evidence_chunk_id"] is None

    assert FakeRuleBasedFallbackProvider.last_input is not None
    assert (
        FakeRuleBasedFallbackProvider.last_input.claim_text
        == "Orion completed the Zephyr project in 2025."
    )
    assert FakeRuleBasedFallbackProvider.last_input.evidence_candidates == []