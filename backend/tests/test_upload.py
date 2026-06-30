from fastapi.testclient import TestClient
from app.main import app
import fitz

client = TestClient(app)

def test_upload_non_pdf_file_rejected():
    files = {
        "file":(
            "test.txt",
            b"This is not a PDF file",
            "text/plain"
        )
    }

    response = client.post("/upload/pdf", files=files)

    assert response.status_code == 400
    assert response.json()["error"]["message"] == ("Invalid file type. Only PDF files are allowed.")

def test_upload_pdf_success():
    pdf_document = fitz.open()
    page = pdf_document.new_page()
    page.insert_text((72, 72),"This PDF contains test content for upload parsing.")

    pdf_bytes = pdf_document.tobytes()
    pdf_document.close()

    files = {
        "file": (
            "test_upload.pdf",
            pdf_bytes,
            "application/pdf"
        )
    }

    response = client.post("/upload/pdf", files=files)

    assert response.status_code == 200

    result = response.json()

    assert "document_id" in result
    assert result["filename"] == "test_upload.pdf"
    assert result["page_count"] >= 1
    assert result["chunk_count"] >= 1

def test_uploaded_pdf_creates_document_and_chunks():
    pdf_document = fitz.open()
    page = pdf_document.new_page()
    page.insert_text((72,72),"orion upload integration test content")

    pdf_byte = pdf_document.tobytes()
    pdf_document.close()

    files = {
        "file":(
            "integration_upload.pdf",
            pdf_byte,
            "application/pdf"
        )
    }

    upload_response = client.post("/upload/pdf", files=files)

    assert upload_response.status_code == 200

    upload_result = upload_response.json()
    document_id = upload_result["document_id"]

    document_response = client.get(f"/documents/{document_id}")

    assert document_response.status_code == 200

    document = document_response.json()
    assert document["id"] == document_id
    assert document["filename"] == "integration_upload.pdf"

    chunks_response = client.get(f"/documents/{document_id}/chunks/")

    assert chunks_response.status_code == 200

    chunks = chunks_response.json()
    assert isinstance(chunks, list)
    assert len(chunks) >= 1

    combined_content = " ".join(chunk["content"] for chunk in chunks)

    assert "orion upload integration test content" in combined_content

def test_upload_missing_file():
    response = client.post("/upload/pdf")

    assert response.status_code == 422
    result = response.json()
    assert result["error"]["code"] == "validation_error"
    assert result["error"]["message"] == "Request validation failed"
    assert isinstance(result["error"]["fields"], list)
    assert len(result["error"]["fields"]) >= 1