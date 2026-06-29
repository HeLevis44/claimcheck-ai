from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_document():
    payload = {
        "filename": "test_document.pdf",
        "file_type": "pdf"
    }

    response = client.post("/documents/",json=payload)

    assert response.status_code == 200
    document = response.json()
    assert "id" in document
    assert document["filename"] == payload["filename"]
    assert document["file_type"] == payload["file_type"]
    assert "created_at" in document

def test_get_document_by_id():
    payload = {
        "filename": "lookup_document.pdf",
        "file_type": "pdf"
    }

    create_response = client.post("/documents/", json=payload)
    assert create_response.status_code == 200

    created_document = create_response.json()
    document_id = created_document["id"]

    response = client.get(f"/documents/{document_id}")

    assert response.status_code == 200

    document = response.json()
    assert document["id"] == document_id
    assert document["filename"] == payload["filename"]
    assert document["file_type"] == payload["file_type"]

def test_get_documents_list():
    payload = {
        "filename": "list_document.pdf",
        "file_type": "pdf"
    }

    create_response = client.post("/documents/", json=payload)
    assert create_response.status_code == 200

    created_document = create_response.json()

    response = client.get("/documents/")

    assert response.status_code == 200

    documents = response.json()
    assert isinstance(documents, list)

    document_ids = [document["id"] for document in documents]

    assert created_document["id"] in document_ids

def test_get_missing_document():
    response = client.get("/documents/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Document not found"

def test_create_document_chunk():
    document_payload = {
        "filename": "chunk_document.pdf",
        "file_type": "pdf"
    }

    document_response = client.post("/documents/", json=document_payload)
    assert document_response.status_code == 200

    document = document_response.json()
    document_id = document["id"]

    chunk_payload = {
        "page_number": 1,
        "chunk_index": 0,
        "content": "This is a test document chunk."
    }

    response = client.post(f"/documents/{document_id}/chunks/", json=chunk_payload)

    assert response.status_code == 200

    chunk = response.json()
    assert "id" in chunk
    assert chunk["document_id"] == document_id
    assert chunk["page_number"] == chunk_payload["page_number"]
    assert chunk["chunk_index"] == chunk_payload["chunk_index"]
    assert chunk["content"] == chunk_payload["content"]

def test_get_document_chunks_list():
    document_payload = {
        "filename": "chunks_list_document.pdf",
        "file_type": "pdf"
    }

    document_response = client.post("/documents/", json=document_payload)
    assert document_response.status_code == 200

    document = document_response.json()
    document_id = document["id"]

    chunk_payload = {
        "page_number": 1,
        "chunk_index": 0,
        "content": "This chunk should appear in the document chunk list."
    }

    create_chunk_response = client.post(f"/documents/{document_id}/chunks/",json=chunk_payload)
    assert create_chunk_response.status_code == 200

    created_chunk = create_chunk_response.json()

    response = client.get(f"/documents/{document_id}/chunks/")

    assert response.status_code == 200

    chunks = response.json()
    assert isinstance(chunks,list)

    chunk_ids = [chunk["id"] for chunk in chunks]
    assert created_chunk["id"] in chunk_ids

def test_create_chunk_for_missing_document():
    chunk_payload = {
        "page_number": 1,
        "chunk_index": 0,
        "content": "This chunk should not be created."
    }

    response = client.post("/documents/999999/chunks/",json = chunk_payload)

    assert response.status_code == 404
    assert response.json()["detail"] == "Document not found"

def test_get_chunks_for_missing_document():
    response = client.get("/documents/999999/chunks/")

    assert response.status_code == 404
    assert response.json()["detail"] == "Document not found"

def test_create_document_missing_required_field():
    payload = {
        "file_type": "pdf"
    }

    response = client.post("/documents/", json=payload)
    assert response.status_code == 422

def test_create_chunk_missing_required_field():
    document_payload = {
        "filename": "missing_content_chunk_document.pdf",
        "file_type": "pdf"
    }
        
    document_response = client.post("/documents/", json=document_payload)
    assert document_response.status_code == 200

    document_id = document_response.json()["id"]

    chunk_payload = {
        "page_number": 1,
        "chunk_index": 0
    }

    response = client.post(
        f"/documents/{document_id}/chunks/",
        json=chunk_payload
    )

    assert response.status_code == 422

def test_get_documents_respects_limit():
    for index in range(3):
        payload = {
            "filename": f"limit_document_{index}.pdf",
            "file_type": "pdf",
        }

        create_response = client.post("/documents/", json=payload)
        assert create_response.status_code == 200

    response = client.get("/documents/?limit=2")

    assert response.status_code == 200

    documents = response.json()
    assert isinstance(documents, list)
    assert len(documents) == 2

def test_get_documents_respects_offset():
    created_document_ids = []

    for index in range(3):
        payload = {
            "filename": f"offset_document_{index}.pdf",
            "file_type": "pdf",
        }

        create_response = client.post("/documents/", json=payload)
        assert create_response.status_code == 200

        created_document_ids.append(create_response.json()["id"])

    response = client.get("/documents/?limit=2&offset=1")

    assert response.status_code == 200

    documents = response.json()
    assert isinstance(documents, list)
    assert len(documents) == 2

    returned_document_ids = [document["id"] for document in documents]

    assert created_document_ids[-1] not in returned_document_ids

def test_get_documents_rejects_zero_limit():
    response = client.get("/documents/?limit=0")

    assert response.status_code == 422

def test_get_documents_rejects_negative_offset():
    response = client.get("/documents/?offset=-1")

    assert response.status_code == 422


