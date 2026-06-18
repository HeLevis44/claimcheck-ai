This project is currently under active development.
# ClaimCheck AI

ClaimCheck AI is a source-grounded claim verification backend. It helps users check whether a written claim is supported by evidence from uploaded PDF documents.

Users can upload source PDFs, the backend parses and chunks the document text, and each claim can be matched against relevant evidence chunks. The current MVP supports ranked keyword-based evidence retrieval and rule-based claim verification.

## Problem

AI-generated writing often contains unsupported claims, misleading citations, or fabricated references. Even when a source document is provided, the cited document may not actually support the claim.

ClaimCheck AI addresses this problem by grounding claims in uploaded source documents and returning evidence-linked verification results.

## Current MVP Features

- Upload source PDF documents
- Parse PDF text using PyMuPDF
- Split PDF text into overlapping chunks
- Store documents and chunks in PostgreSQL
- Create and store claims
- Retrieve relevant evidence chunks for each claim
- Rank evidence chunks by keyword match score
- Automatically verify a claim using a rule-based verifier
- Store verification results in the database
- Query verification results by claim or by result ID
- Test all backend APIs through FastAPI Swagger UI

## Current Verification Logic

The current MVP uses a simple rule-based verifier:

- If no evidence is found:
  - status: `not_enough_evidence`
  - confidence: `0.2`
- If the top evidence chunk has a keyword match score of 3 or higher:
  - status: `likely_supported`
  - confidence: `0.8`
- If the top evidence chunk has a keyword match score below 3:
  - status: `weak_evidence`
  - confidence: `0.5`

This rule-based system is intentionally simple and will later be replaced or enhanced with embedding-based retrieval and LLM-based verification.

## Tech Stack

### Backend

- FastAPI
- Python
- SQLAlchemy
- Pydantic
- PostgreSQL
- PyMuPDF

### DevOps and Tooling

- Docker
- Docker Compose
- Environment variables
- FastAPI Swagger UI
- Git and GitHub

### Planned AI Components

- Embedding-based semantic retrieval
- pgvector for vector similarity search
- LLM-based claim extraction
- LLM-based evidence-aware verification
- Structured JSON outputs

## Backend Architecture

```text
FastAPI Backend
  |
  +--> API Layer
  |     +--> documents.py
  |     +--> chunks.py
  |     +--> upload.py
  |     +--> claims.py
  |     +--> verification.py
  |
  +--> Service Layer
  |     +--> retrieval.py
  |     +--> verification.py
  |
  +--> Database Layer
  |     +--> SQLAlchemy models
  |     +--> PostgreSQL
  |
  +--> Schemas
        +--> Pydantic request and response models
```

## Current Data Flow

```text
Upload PDF
  ↓
Parse PDF text
  ↓
Split text into chunks
  ↓
Store document and chunks in PostgreSQL
  ↓
Create claim
  ↓
Retrieve ranked evidence chunks
  ↓
Run rule-based verification
  ↓
Store and return verification result
```

## Main API Endpoints

### Health Check

```text
GET /health
GET /health/db
```

### Documents

```text
POST /documents/
GET /documents/
GET /documents/{document_id}
GET /documents/{document_id}/chunks/
```

### PDF Upload

```text
POST /upload/pdf
```

Uploads a PDF, extracts text, splits it into chunks, and stores the document and chunks in PostgreSQL.

### Claims

```text
POST /claims/
GET /claims/
GET /claims/{claim_id}
GET /claims/{claim_id}/evidence
POST /claims/{claim_id}/verify
```

`GET /claims/{claim_id}/evidence` returns ranked evidence chunks with a keyword match score.

`POST /claims/{claim_id}/verify` automatically retrieves evidence, applies the rule-based verifier, stores a verification result, and returns it.

### Verification Results

```text
POST /verification-results/
GET /verification-results/
GET /verification-results/claim/{claim_id}
GET /verification-results/{verification_id}
```

These endpoints support manual creation and querying of verification results.

## Example Workflow

1. Upload a PDF through `POST /upload/pdf`.
2. Check the stored chunks with `GET /documents/{document_id}/chunks/`.
3. Create a claim with `POST /claims/`.
4. Retrieve evidence with `GET /claims/{claim_id}/evidence`.
5. Automatically verify the claim with `POST /claims/{claim_id}/verify`.
6. View saved verification results with `GET /verification-results/claim/{claim_id}`.

## Project Structure

```text
backend/
  app/
    api/
      claims.py
      documents.py
      health.py
      upload.py
      verification.py
    core/
      config.py
    db/
      database.py
      init_db.py
      models.py
    schemas/
      claim.py
      chunk.py
      document.py
      evidence.py
      verification.py
    services/
      retrieval.py
      verification.py
    main.py
  requirements.txt

docker-compose.yml
README.md
```

## Development Status

### Completed

- FastAPI backend setup
- PostgreSQL connection with SQLAlchemy
- Database models for documents, chunks, claims, and verification results
- PDF upload and parsing
- Text chunking with overlap
- Claim creation and query APIs
- Ranked keyword-based evidence retrieval
- Rule-based automatic claim verification
- Verification result creation and query APIs
- Service layer refactor for retrieval and verification logic

### Next Steps

- Add stronger retrieval scoring
- Add embedding generation for document chunks
- Add pgvector similarity search
- Add LLM-based claim extraction
- Add LLM-based verification with structured JSON output
- Add frontend dashboard
- Add authentication and user-specific documents
- Add tests for core API endpoints

## Local Development

Start the PostgreSQL database:

```bash
docker compose up -d
```

Start the FastAPI backend:

```bash
cd backend
uvicorn app.main:app --reload
```

Open the API docs:

```text
http://127.0.0.1:8000/docs
```

## Status

This project is under active development. The current version is a backend MVP with source document ingestion, ranked evidence retrieval, and rule-based claim verification.