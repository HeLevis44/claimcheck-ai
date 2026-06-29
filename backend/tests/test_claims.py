from fastapi.testclient import TestClient
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
    assert response.json()["detail"] == "Claim not found"

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