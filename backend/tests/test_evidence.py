from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_claim_evidence(sample_claim_with_chunk):
    claim = sample_claim_with_chunk["claim"]
    chunk = sample_claim_with_chunk["chunk"]

    response = client.get(f"/claims/{claim.id}/evidence")

    assert response.status_code == 200
    evidences = response.json()
    assert isinstance(evidences,list)
    assert evidences

    matching_evidence = next(
        (evidence for evidence in evidences if evidence["chunk_id"] == chunk.id),
        None
    )

    assert matching_evidence is not None
    assert matching_evidence["score"] >= 1

def test_evidence_is_ranked_by_score(sample_claim_with_ranked_chunks):
    claim = sample_claim_with_ranked_chunks["claim"]
    high_score_chunk = sample_claim_with_ranked_chunks["high_score_chunk"]
    low_score_chunk = sample_claim_with_ranked_chunks["low_score_chunk"]

    response = client.get(f"/claims/{claim.id}/evidence")

    assert response.status_code == 200

    evidences = response.json()

    assert isinstance(evidences, list)
    assert len(evidences) >= 2

    assert evidences[0]["chunk_id"] == high_score_chunk.id
    assert evidences[0]["score"] > evidences[1]["score"]

    returned_chunk_ids = [evidence["chunk_id"] for evidence in evidences]
    assert low_score_chunk.id in returned_chunk_ids

def test_evidence_for_missing_claim():
    response = client.get("/claims/999999/evidence")
    assert response.status_code == 404
    assert response.json()["error"]["message"] == "Claim not found"