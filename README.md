# ClaimCheck AI

ClaimCheck AI is a source-grounded claim verification backend for checking whether a written claim is supported by evidence from uploaded PDF documents.

Users can upload source PDFs, extract and chunk document text, create claims, retrieve ranked evidence candidates, and save evidence-linked verification results. The current project is a backend MVP designed to support a later frontend workflow.

## Problem

AI-generated writing can contain unsupported claims, misleading citations, or fabricated references. Even when a source document is available, the document may not actually support the claim.

ClaimCheck AI addresses this by grounding verification in uploaded source documents and linking each result to a selected evidence chunk when evidence is available.

## Current MVP Features

- Upload PDF documents through FastAPI
- Extract PDF text with PyMuPDF
- Split extracted text into document chunks
- Store documents, chunks, claims, and verification results in PostgreSQL
- Create, retrieve, search, and paginate claims
- Create, retrieve, search, and paginate documents
- Retrieve ranked evidence chunks with keyword-based scoring
- Run rule-based claim verification
- Support an optional OpenAI verification mode through a provider interface
- Fall back to rule-based verification when the OpenAI provider fails
- Store verification status, confidence, reasoning, and optional evidence chunk linkage
- Return frontend-ready verification detail data
- Use a shared pagination response format
- Return consistent HTTP and validation error responses
- Test core backend behavior with pytest, FastAPI TestClient, fake providers, and mocked provider behavior

## Verification Modes

`POST /claims/{claim_id}/verify` supports two modes.

### `rule_based`

This is the default mode. It does not require an API key and preserves the original MVP behavior.

The rule-based verifier uses retrieval scores:

- No evidence found:
  - status: `not_enough_evidence`
  - confidence: `0.2`
- Top evidence score is `3` or higher:
  - status: `likely_supported`
  - confidence: `0.8`
- Top evidence score is below `3`:
  - status: `weak_evidence`
  - confidence: `0.5`

### `openai`

This mode converts the claim and retrieved evidence candidates into an `LLMVerificationInput` and sends it to `OpenAIVerificationProvider`.

The provider requests a structured verification result with the following fields:

```json
{
  "status": "likely_supported",
  "confidence": 0.9,
  "reasoning": "The selected evidence directly supports the claim.",
  "evidence_chunk_id": 101
}
```

The provider validates that:

- `status` is one of `likely_supported`, `weak_evidence`, or `not_enough_evidence`
- `confidence` is between `0` and `1`
- `reasoning` is not empty
- `evidence_chunk_id` is one of the retrieved evidence chunk IDs or `null`

If the OpenAI provider cannot initialize or verify the claim, the endpoint automatically uses `RuleBasedFallbackProvider` and still returns a verification result.

## Tech Stack

### Backend

- Python
- FastAPI
- Pydantic v2
- SQLAlchemy 2
- PostgreSQL
- PyMuPDF
- OpenAI Python SDK

### Tooling

- Docker and Docker Compose
- Uvicorn
- pytest
- httpx / FastAPI TestClient
- Git and GitHub

## Backend Architecture

```text
FastAPI Backend
  |
  +--> API Layer
  |     +--> health.py
  |     +--> documents.py
  |     +--> chunks.py
  |     +--> upload.py
  |     +--> claims.py
  |     +--> verification.py
  |
  +--> Service Layer
  |     +--> retrieval.py
  |     +--> verification.py
  |     +--> llm_verification.py
  |     +--> verification_detail.py
  |     +--> pagination.py
  |
  +--> Schema Layer
  |     +--> document.py
  |     +--> claim.py
  |     +--> verification.py
  |     +--> llm_verification.py
  |     +--> pagination.py
  |     +--> error.py
  |
  +--> Database Layer
        +--> SQLAlchemy models
        +--> PostgreSQL
```

## Current Data Flow

```text
Upload PDF
  ↓
Extract PDF text
  ↓
Split text into chunks
  ↓
Store document and chunks in PostgreSQL
  ↓
Create claim
  ↓
Retrieve ranked evidence chunks
  ↓
Choose verification mode
  ├── rule_based
  └── openai
        ↓ on provider failure
      rule-based fallback
  ↓
Store and return verification result
```

## Main API Endpoints

### Health

```text
GET /health
GET /health/db
```

### Documents and Chunks

```text
POST /documents/
GET /documents/
GET /documents/{document_id}
POST /documents/{document_id}/chunks/
GET /documents/{document_id}/chunks/
```

`GET /documents/` supports:

```text
?q=keyword
?limit=20
?offset=0
```

### PDF Upload

```text
POST /upload/pdf
```

This endpoint uploads a PDF, extracts text, creates a `Document`, splits the text into chunks, and stores `DocumentChunk` rows.

### Claims

```text
POST /claims/
GET /claims/
GET /claims/{claim_id}
GET /claims/{claim_id}/evidence
POST /claims/{claim_id}/verify
```

`GET /claims/` supports:

```text
?q=keyword
?limit=20
?offset=0
```

`GET /claims/{claim_id}/evidence` returns ranked evidence chunks with keyword match scores.

#### Verify with the default rule-based mode

```bash
curl -X POST http://127.0.0.1:8000/claims/1/verify
```

#### Verify with OpenAI mode

```bash
curl -X POST http://127.0.0.1:8000/claims/1/verify \
  -H "Content-Type: application/json" \
  -d '{"mode": "openai"}'
```

Supported values:

```text
rule_based
openai
```

If no request body is sent, the endpoint defaults to `rule_based`.

### Verification Results

```text
POST /verification-results/
GET /verification-results/
GET /verification-results/{verification_id}
GET /verification-results/claim/{claim_id}
GET /verification-results/{verification_id}/detail
```

The verification-result list endpoints support `limit` and `offset`.

`GET /verification-results/{verification_id}/detail` returns frontend-ready data:

```json
{
  "verification": {
    "id": 1,
    "status": "likely_supported",
    "confidence": 0.8,
    "reasoning": "..."
  },
  "claim": {
    "id": 1,
    "claim_text": "...",
    "source_text": "..."
  },
  "evidence": {
    "id": 1,
    "document_id": 1,
    "filename": "example.pdf",
    "page_number": 1,
    "chunk_index": 0,
    "content": "..."
  }
}
```

When no evidence is selected, `evidence` is `null`.

## Shared Pagination Format

Paginated list endpoints return:

```json
{
  "items": [],
  "total": 0,
  "limit": 20,
  "offset": 0,
  "has_more": false
}
```

## Error Response Format

### HTTP errors

```json
{
  "error": {
    "code": "http_error",
    "message": "Claim not found"
  }
}
```

### Validation errors

```json
{
  "error": {
    "code": "validation_error",
    "message": "Request validation failed",
    "fields": []
  }
}
```

## Example Workflow

1. Upload a PDF through `POST /upload/pdf`.
2. Inspect stored chunks through `GET /documents/{document_id}/chunks/`.
3. Create a claim through `POST /claims/`.
4. Inspect ranked evidence through `GET /claims/{claim_id}/evidence`.
5. Verify the claim through `POST /claims/{claim_id}/verify`.
6. Query saved results through `GET /verification-results/claim/{claim_id}`.
7. Retrieve display-ready detail through `GET /verification-results/{verification_id}/detail`.

## Project Structure

```text
backend/
  app/
    api/
      health.py
      documents.py
      chunks.py
      upload.py
      claims.py
      verification.py
    db/
      database.py
      models.py
    schemas/
      document.py
      claim.py
      verification.py
      llm_verification.py
      pagination.py
      error.py
    services/
      retrieval.py
      verification.py
      llm_verification.py
      verification_detail.py
      pagination.py
    main.py
  tests/
    conftest.py
    test_health.py
    test_documents.py
    test_upload.py
    test_claims.py
    test_evidence.py
    test_verification.py
    test_llm_verification.py
  requirements.txt
  .env.example

docker-compose.yml
README.md
```

## Local Development

### 1. Start PostgreSQL

From the project root:

```bash
docker compose up -d
```

### 2. Install backend dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 3. Start the backend

```bash
uvicorn app.main:app --reload
```

### 4. Open API documentation

```text
http://127.0.0.1:8000/docs
```

### 5. Run tests

Run tests from the backend directory so pytest does not collect unrelated projects from the home directory:

```bash
cd ~/Desktop/claim_ai/backend
python -m pytest
```

## Environment Variables

`.env.example` documents the expected OpenAI variable:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

Do not commit a real API key. Store it in a local `.env` file excluded by `.gitignore`, or export the variable in your shell before starting the backend.

The default `rule_based` mode does not require an OpenAI API key. `openai` mode requires a valid key and provider access. If the provider fails, the endpoint falls back to rule-based verification.

## Development Status

### Completed

- FastAPI backend setup
- PostgreSQL connection with SQLAlchemy
- Models for documents, chunks, claims, and verification results
- PDF upload, parsing, and text chunking
- Claims and document APIs
- Ranked keyword-based evidence retrieval
- Rule-based verification
- Manual verification-result APIs
- Verification detail endpoint
- Shared pagination helper and paginated list responses
- Search for claims and documents
- Unified HTTP and validation error responses
- Verification status enum
- LLM verification input and output schemas
- Provider interface, fake provider tests, and rule-based adapter
- OpenAI verification provider with structured output parsing
- OpenAI provider mock tests and evidence chunk validation
- Verification mode selection: `rule_based` or `openai`
- Automatic rule-based fallback when OpenAI verification fails

### Next Steps

1. Environment and startup-flow cleanup
2. Final backend test pass and release commit
3. Frontend project setup and API client
4. PDF upload workflow in the frontend
5. Claims list with search and pagination
6. Verification detail page
7. Loading, error, and empty states

### V2 Backlog

The following are intentionally out of scope for the current MVP:

- Status filters and more advanced document filters
- More complex search behavior
- Authentication and user-specific documents
- Database migrations
- pgvector and semantic retrieval
- Embedding-based evidence ranking
- Additional API optimization and abstraction

## Status

This project is under active development. The current version is a backend MVP with PDF ingestion, ranked evidence retrieval, rule-based verification, optional OpenAI verification mode, provider fallback, pagination, search, standardized errors, and test coverage for core API behavior.