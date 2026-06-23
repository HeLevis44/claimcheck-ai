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