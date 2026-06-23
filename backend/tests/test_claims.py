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
    claims = response.json()
    assert isinstance(claims, list)

    claim_ids = [claim["id"] for claim in claims]
    assert created_claim["id"] in claim_ids

def test_create_claim_missing_required_field():
    payload = {
        "source_text": "Test source text."
    }
    response = client.post("/claims/", json=payload)
    assert response.status_code == 422