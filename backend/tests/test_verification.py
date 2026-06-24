from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_verification_check(sample_claim_with_chunk):
    claim = sample_claim_with_chunk["claim"]
    chunk = sample_claim_with_chunk["chunk"]

    response = client.post(f"/claims/{claim.id}/verify")

    assert response.status_code == 200

    verification_result = response.json()
    assert "id" in verification_result
    assert verification_result["claim_id"] == claim.id
    assert verification_result["evidence_chunk_id"] is not None
    assert verification_result["status"] in ["likely_supported", "weak_evidence"]
    assert isinstance(verification_result["confidence"], float)
    assert verification_result["reasoning"]

def test_verification_without_evidence(sample_claim_without_evidence):
    claim = sample_claim_without_evidence
    response = client.post(f"/claims/{claim.id}/verify")

    assert response.status_code == 200
    verification_result = response.json()

    assert verification_result["claim_id"] == claim.id
    assert verification_result["evidence_chunk_id"] is None
    assert verification_result["status"] == "not_enough_evidence"
    assert verification_result["confidence"] == 0.2
    assert verification_result["reasoning"] == "No relevant evidence chunks were found."

def test_get_verification_results_by_claim(sample_claim_with_chunk):
    claim = sample_claim_with_chunk["claim"]

    create_response = client.post(f"/claims/{claim.id}/verify")
    assert create_response.status_code == 200

    created_result = create_response.json()

    response = client.get(f"/verification-results/claim/{claim.id}")

    assert response.status_code == 200

    verification_results = response.json()
    assert isinstance(verification_results, list)

    matching_result = next(
        (
            result
            for result in verification_results
            if result["id"] == created_result["id"]
        ),
        None
    )

    assert matching_result is not None
    assert matching_result["claim_id"] == claim.id

def test_get_verification_result_by_id(sample_claim_with_chunk):
    claim = sample_claim_with_chunk["claim"]

    create_response = client.post(f"/claims/{claim.id}/verify")
    assert create_response.status_code == 200

    created_result = create_response.json()

    response = client.get(f"/verification-results/{created_result['id']}")

    assert response.status_code == 200

    verification_result = response.json()
    assert verification_result["id"] == created_result["id"]
    assert verification_result["claim_id"] == claim.id


def test_get_verification_results_for_missing_claim():
    response = client.get("/verification-results/claim/999999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Claim not found"

def test_verification_uses_highest_scoring_evidence(sample_claim_with_ranked_chunks):
    claim = sample_claim_with_ranked_chunks["claim"]
    high_score_chunk = sample_claim_with_ranked_chunks["high_score_chunk"]
    response = client.post(f"/claims/{claim.id}/verify")

    assert response.status_code == 200

    verification_result = response.json()

    assert verification_result["claim_id"] == claim.id
    assert verification_result["evidence_chunk_id"] == high_score_chunk.id
    assert verification_result["status"] == "likely_supported"
    assert verification_result["confidence"] == 0.8

def test_get_missing_verification_result():
    response = client.get("/verification-results/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Verification result not found"

def test_create_verification_result_manually(sample_claim_with_chunk):
    claim = sample_claim_with_chunk["claim"]

    chunk = sample_claim_with_chunk["chunk"]

    payload = {
        "claim_id": claim.id,
        "evidence_chunk_id": chunk.id,
        "status": "supported",
        "confidence": 0.9,
        "reasoning": "The evidence chunk supports the claim."
    }
    response = client.post("/verification-results/", json=payload)

    assert response.status_code == 200

    verification_result = response.json()

    assert "id" in verification_result
    assert verification_result["claim_id"] == claim.id
    assert verification_result["evidence_chunk_id"] == chunk.id
    assert verification_result["status"] == payload["status"]
    assert verification_result["confidence"] == payload["confidence"]
    assert verification_result["reasoning"] == payload["reasoning"]

def test_create_verification_result_with_missing_claim():
    payload = {
        "claim_id": 999999,
        "evidence_chunk_id": None,
        "status": "unsupported",
        "confidence": 0.1,
        "reasoning": "The referenced claim does not exist."
    }

    response = client.post("/verification-results/", json=payload)

    assert response.status_code == 404
    assert response.json()["detail"] == "Claim not found"

def test_create_verification_result_with_missing_chunk(sample_claim_with_chunk):
    claim = sample_claim_with_chunk["claim"]

    payload = {
        "claim_id": claim.id,
        "evidence_chunk_id": 999999,
        "status": "unsupported",
        "confidence": 0.1,
        "reasoning": "The referenced evidence chunk does not exist."
    }

    response = client.post("/verification-results/", json=payload)
    assert response.status_code == 404
    assert response.json()["detail"] == "Evidence chunk not found"

def test_create_verification_result_without_evidence(sample_claim_without_evidence):
    claim = sample_claim_without_evidence

    payload = {
        "claim_id": claim.id,
        "evidence_chunk_id": None,
        "status": "not_enough_evidence",
        "confidence": 0.2,
        "reasoning": "No relevant evidence chunks were found."
    }

    response = client.post("/verification-results/", json=payload)

    assert response.status_code == 200
    verification_result = response.json()

    assert "id" in verification_result
    assert verification_result["claim_id"] == claim.id
    assert verification_result["evidence_chunk_id"] is None
    assert verification_result["status"] == payload["status"]
    assert verification_result["confidence"] == payload["confidence"]
    assert verification_result["reasoning"] == payload["reasoning"]

def test_get_all_verification_results(sample_claim_with_chunk):
    claim = sample_claim_with_chunk["claim"]

    create_response = client.post(f"/claims/{claim.id}/verify")
    assert create_response.status_code == 200

    created_result = create_response.json()

    response = client.get("/verification-results/")

    assert response.status_code == 200

    verification_results = response.json()
    assert isinstance(verification_results, list)

    result_ids = [
        verification_result["id"]
        for verification_result in verification_results
    ]

    assert created_result["id"] in result_ids

def test_verify_missing_claim():
    response = client.post("/claims/999999/verify")

    assert response.status_code == 404
    assert response.json()["detail"] == "Claim not found"

def test_create_verification_result_missing_required_field(
    sample_claim_without_evidence
):
    claim = sample_claim_without_evidence

    payload = {
        "claim_id": claim.id,
        "evidence_chunk_id": None,
        "confidence": 0.2,
        "reasoning": "Missing status should be rejected."
    }

    response = client.post("/verification-results/", json=payload)

    assert response.status_code == 422

def test_get_all_verification_results_when_empty():
    response = client.get("/verification-results/")

    assert response.status_code == 200
    assert response.json() == []