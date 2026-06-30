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

    result = response.json()

    assert isinstance(result, dict)
    assert "items" in result
    assert "total" in result
    assert "limit" in result
    assert "offset" in result
    assert "has_more" in result

    matching_result = next(
    (
        verification_result
        for verification_result in result["items"]
        if verification_result["id"] == created_result["id"]
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
    assert response.json()["error"]["message"] == "Claim not found"

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
    assert response.json()["error"]["message"] == "Verification result not found"

def test_create_verification_result_manually(sample_claim_with_chunk):
    claim = sample_claim_with_chunk["claim"]

    chunk = sample_claim_with_chunk["chunk"]

    payload = {
        "claim_id": claim.id,
        "evidence_chunk_id": chunk.id,
        "status": "likely_supported",
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
        "status": "weak_evidence",
        "confidence": 0.1,
        "reasoning": "The referenced claim does not exist."
    }

    response = client.post("/verification-results/", json=payload)

    assert response.status_code == 404
    assert response.json()["error"]["message"] == "Claim not found"

def test_create_verification_result_with_missing_chunk(sample_claim_with_chunk):
    claim = sample_claim_with_chunk["claim"]

    payload = {
        "claim_id": claim.id,
        "evidence_chunk_id": 999999,
        "status": "weak_evidence",
        "confidence": 0.1,
        "reasoning": "The referenced evidence chunk does not exist."
    }

    response = client.post("/verification-results/", json=payload)
    assert response.status_code == 404
    assert response.json()["error"]["message"] == "Evidence chunk not found"

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

    result = response.json()
    assert isinstance(result, dict)
    assert "items" in result
    assert "total" in result
    assert "limit" in result
    assert "offset" in result
    assert "has_more" in result

    result_ids = [
        verification_result["id"]
        for verification_result in result["items"]
    ]

    assert created_result["id"] in result_ids

def test_verify_missing_claim():
    response = client.post("/claims/999999/verify")

    assert response.status_code == 404
    assert response.json()["error"]["message"] == "Claim not found"

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
    result = response.json()
    assert isinstance(result, dict)
    assert result["items"] == []
    assert result["total"] == 0
    assert result["limit"] == 20
    assert result["offset"] == 0
    assert result["has_more"] is False


def test_get_verification_result_detail_with_evidence(sample_claim_with_chunk):
    claim = sample_claim_with_chunk["claim"]
    chunk = sample_claim_with_chunk["chunk"]
    create_response = client.post(f"/claims/{claim.id}/verify")

    assert create_response.status_code == 200
    create_result = create_response.json()

    response = client.get(f"/verification-results/{create_result['id']}/detail")
    assert response.status_code == 200

    detail = response.json()

    assert detail["verification"]["id"] == create_result["id"]
    assert detail["verification"]["status"] == create_result["status"]
    assert detail["verification"]["confidence"] == create_result["confidence"]

    assert detail["claim"]["id"] == claim.id
    assert detail["claim"]["claim_text"] == claim.claim_text
    assert detail["claim"]["source_text"] == claim.source_text

    assert detail["evidence"] is not None
    assert detail["evidence"]["id"] == chunk.id
    assert detail["evidence"]["document_id"] == chunk.document_id
    assert detail["evidence"]["page_number"] == chunk.page_number
    assert detail["evidence"]["chunk_index"] == chunk.chunk_index
    assert detail["evidence"]["content"] == chunk.content

    assert detail["evidence"]["filename"] == chunk.document.filename

def test_get_verification_result_detail_without_evidence(sample_claim_without_evidence):
    claim = sample_claim_without_evidence

    create_response = client.post(f"/claims/{claim.id}/verify")
    assert create_response.status_code == 200

    create_result = create_response.json()
    
    response = client.get(f"/verification-results/{create_result['id']}/detail")
    assert response.status_code == 200

    detail = response.json()
    assert detail["verification"]["id"] == create_result["id"]
    assert detail["claim"]["id"] == claim.id
    assert detail["claim"]["claim_text"] == claim.claim_text
    
    assert detail['evidence'] is None

def test_get_missing_verification_result_detail():
    response = client.get("/verification-results/999999/detail")

    assert response.status_code == 404
    assert response.json()["error"]["message"] == "Verification result not found"

def test_get_verification_results_respects_limit(sample_claim_with_chunk):
    claim = sample_claim_with_chunk["claim"]

    for _ in range(3):
        create_response = client.post(f"/claims/{claim.id}/verify")
        assert create_response.status_code == 200

    response = client.get("/verification-results/?limit=2")
    assert response.status_code == 200

    result = response.json()
    assert isinstance(result, dict)
    assert result["total"] == 3
    assert result["limit"] == 2
    assert result["offset"] == 0
    assert len(result["items"]) == 2
    assert result["has_more"] is True

def test_get_verification_results_respects_offset(sample_claim_with_chunk):
    claim = sample_claim_with_chunk["claim"]

    created_result_ids = []

    for _ in range(3):
        create_response = client.post(f"/claims/{claim.id}/verify")
        assert create_response.status_code == 200

        created_result_ids.append(create_response.json()["id"])

    response = client.get("/verification-results/?limit=2&offset=1")

    assert response.status_code == 200

    result = response.json()

    assert isinstance(result, dict)
    assert result["total"] == 3
    assert result["limit"] == 2
    assert result["offset"] == 1
    assert len(result["items"]) == 2
    assert result["has_more"] is False

    returned_result_ids = [
        verification_result["id"]
        for verification_result in result["items"]
    ]

    assert created_result_ids[-1] not in returned_result_ids

def test_get_verification_results_rejects_zero_limit():
    response = client.get("/verification-results/?limit=0")

    assert response.status_code == 422

def test_get_verification_results_rejects_negative_offset():
    response = client.get("/verification-results/?offset=-1")

    assert response.status_code == 422

def test_get_verification_results_for_claim_respects_limit(
    sample_claim_with_chunk,
):
    claim = sample_claim_with_chunk["claim"]

    for _ in range(3):
        create_response = client.post(f"/claims/{claim.id}/verify")
        assert create_response.status_code == 200

    response = client.get(
        f"/verification-results/claim/{claim.id}?limit=2"
    )

    assert response.status_code == 200

    result = response.json()
    assert isinstance(result, dict)
    assert result["total"] == 3
    assert result["limit"] == 2
    assert result["offset"] == 0
    assert len(result["items"]) == 2
    assert result["has_more"] is True

    assert all(
        verification_result["claim_id"] == claim.id
        for verification_result in result["items"]
    )

def test_get_verification_results_for_claim_respects_offset(
    sample_claim_with_chunk,
):
    claim = sample_claim_with_chunk["claim"]
    created_result_ids = []

    for _ in range(3):
        create_response = client.post(f"/claims/{claim.id}/verify")
        assert create_response.status_code == 200

        created_result_ids.append(create_response.json()["id"])

    response = client.get(
        f"/verification-results/claim/{claim.id}?limit=2&offset=1"
    )

    assert response.status_code == 200

    result = response.json()
    assert isinstance(result, dict)
    assert result["total"] == 3
    assert result["limit"] == 2
    assert result["offset"] == 1
    assert len(result["items"]) == 2
    assert result["has_more"] is False

    returned_result_ids = [
        verification_result["id"]
        for verification_result in result["items"]
    ]

    assert created_result_ids[-1] not in returned_result_ids

    assert all(
        verification_result["claim_id"] == claim.id
        for verification_result in result["items"]
    )

def test_get_verification_results_for_claim_rejects_zero_limit(
    sample_claim_with_chunk,
):
    claim = sample_claim_with_chunk["claim"]

    response = client.get(
        f"/verification-results/claim/{claim.id}?limit=0"
    )

    assert response.status_code == 422

def test_get_verification_results_for_claim_rejects_negative_offset(
    sample_claim_with_chunk,
):
    claim = sample_claim_with_chunk["claim"]

    response = client.get(
        f"/verification-results/claim/{claim.id}?offset=-1"
    )

    assert response.status_code == 422

def test_create_verification_result_rejects_invalid_status(
    sample_claim_without_evidence,
):
    claim = sample_claim_without_evidence

    payload = {
        "claim_id": claim.id,
        "evidence_chunk_id": None,
        "status": "invalid_status",
        "confidence": 0.5,
        "reasoning": "This status should be rejected.",
    }

    response = client.post("/verification-results/", json=payload)

    assert response.status_code == 422

    result = response.json()
    assert result["error"]["code"] == "validation_error"
    assert result["error"]["message"] == "Request validation failed"