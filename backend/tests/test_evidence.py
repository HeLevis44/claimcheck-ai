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