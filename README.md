# ClaimCheck AI

ClaimCheck AI is a full-stack source-grounded claim verification app. Users can upload PDF documents, create written claims, retrieve evidence chunks from uploaded sources, and generate a verification result with status, confidence, reasoning, and evidence linkage.

The project is designed as a practical SDE + AI portfolio project. It combines a FastAPI backend, PostgreSQL persistence, PDF ingestion, evidence retrieval, optional OpenAI verification, and a Next.js frontend workflow.

## Problem

AI-generated writing can contain unsupported claims, misleading citations, or fabricated references. Even when a source document is available, the document may not actually support the claim.

ClaimCheck AI addresses this by grounding verification in uploaded source documents and showing the evidence chunks used to evaluate each claim.

## Current MVP Features

### Frontend

- Dashboard landing page with navigation to the main workflows
- Upload PDF files from the browser
- Display uploaded documents
- Search and paginate uploaded documents
- Create claims from the UI
- Display claim list
- Search and paginate claims
- Select verification mode: `rule_based` or `openai`
- Verify claims and display status, confidence, and reasoning
- Display evidence chunks used for verification
- Show the top 3 evidence chunks by default with expand/collapse support
- Shared React components for cards, search controls, pagination controls, and verification display
- Loading, empty, disabled, and error states for the main workflow
- Back-to-dashboard navigation from workflow pages

### Backend

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

## Tech Stack

### Frontend

- Next.js App Router
- React
- TypeScript
- Tailwind CSS

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

## Application Flow

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
Verify claim
  ├── rule_based
  └── openai
        ↓ on provider failure
      rule-based fallback
  ↓
Display verification result and evidence chunks in the frontend
```

## Frontend Structure

```text
frontend/
  src/
    app/
      globals.css
      layout.tsx
      page.tsx
      documents/
        page.tsx
      claims/
        page.tsx
    components/
      HeaderCard.tsx
      ErrorBanner.tsx
      CreateClaimCard.tsx
      UploadPdfCard.tsx
      DocumentsCard.tsx
      ClaimsCard.tsx
      VerificationModeSelector.tsx
      VerificationResultCard.tsx
      EvidenceCard.tsx
      SearchCard.tsx
      PaginationControls.tsx
    lib/
      api.ts
    types/
      api.ts
```

### Frontend Component Roles

```text
app/page.tsx
  Provides the dashboard landing page and navigation to the main workflows.

app/documents/page.tsx
  Owns document workflow state.
  Handles PDF upload, document search, and document pagination.

app/claims/page.tsx
  Owns claim workflow state.
  Handles claim creation, claim search, pagination, verification mode selection, verification, and evidence retrieval.
```

## Backend Architecture

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

1. Start PostgreSQL and the FastAPI backend.
2. Start the Next.js frontend.
3. Open the dashboard at `http://localhost:3000`.
4. Go to the Documents page.
5. Upload a PDF from the browser.
6. Confirm that the document appears in the uploaded documents list.
7. Search uploaded documents and use pagination controls.
8. Return to the dashboard.
9. Go to the Claims page.
10. Create a claim.
11. Search claims and use pagination controls.
12. Select a verification mode.
13. Click `Verify` on the claim.
14. Review the verification status, confidence, reasoning, and evidence chunks.
15. Expand the evidence list when more than three chunks are returned.

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
cd backend
uvicorn app.main:app --reload
```

Backend runs at:

```text
http://127.0.0.1:8000
```

API docs are available at:

```text
http://127.0.0.1:8000/docs
```

### 4. Install frontend dependencies

```bash
cd frontend
npm install
```

### 5. Configure frontend environment

Create `frontend/.env.local`:

```env
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
```

### 6. Start the frontend

```bash
cd frontend
npm run dev
```

Frontend runs at:

```text
http://localhost:3000
```

### 7. Run backend tests

Run tests from the backend directory so pytest does not collect unrelated projects from the home directory:

```bash
cd ~/Desktop/claim_ai/backend
python -m pytest
```

### 8. Build the frontend

```bash
cd ~/Desktop/claim_ai/frontend
npm run build
```

## Environment Variables

### Backend

`.env.example` documents the expected OpenAI variable:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

Do not commit a real API key. Store it in a local `.env` file excluded by `.gitignore`, or export the variable in your shell before starting the backend.

The default `rule_based` mode does not require an OpenAI API key. `openai` mode requires a valid key and provider access. If the provider fails, the endpoint falls back to rule-based verification.

### Frontend

`frontend/.env.local` should contain:

```env
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
```

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
- Frontend search controls for claims and documents
- Frontend pagination controls for claims and documents
- Unified HTTP and validation error responses
- Verification status enum
- LLM verification input and output schemas
- Provider interface, fake provider tests, and rule-based adapter
- OpenAI verification provider with structured output parsing
- OpenAI provider mock tests and evidence chunk validation
- Verification mode selection: `rule_based` or `openai`
- Automatic rule-based fallback when OpenAI verification fails
- Next.js frontend setup
- Frontend API client and shared TypeScript response types
- PDF upload UI
- Uploaded documents list
- Claim creation UI
- Claims list UI
- Verification result display
- Evidence chunk display with expand/collapse behavior
- Reusable frontend component split, including shared search and pagination components
- Dashboard route and separate documents and claims routes
- Back-to-dashboard navigation on workflow pages

### Next Steps

1. Add a verification detail page
2. Improve PDF upload UX and file selection reset behavior
3. Add screenshots or a short demo GIF to the README
4. Add database migrations for production-style schema management
5. Prepare deployment configuration for a production demo

## Demo Checklist

Use this checklist when recording or presenting the project demo.

1. Start PostgreSQL, the backend, and the frontend.
2. Open the dashboard at `http://localhost:3000`.
3. Go to the Documents page.
   - Upload a PDF.
   - Search uploaded documents.
   - Use Previous and Next pagination controls.
   - Return to the dashboard.
4. Go to the Claims page.
   - Create a new claim.
   - Search claims.
   - Use Previous and Next pagination controls.
   - Select rule-based verification.
   - Verify a claim and review the status, confidence, reasoning, and evidence chunks.
   - Return to the dashboard.
5. Optional OpenAI demo.
   - Set `OPENAI_API_KEY` in the backend environment.
   - Select OpenAI verification mode.
   - Verify a claim and compare the result with rule-based mode.

## Status

This project is under active development. The current version is a full-stack MVP with PDF ingestion, document chunking, claim creation, evidence retrieval, rule-based verification, optional OpenAI verification mode, provider fallback, standardized errors, backend tests, and a polished Next.js frontend with dashboard navigation, document upload, search, pagination, claim creation, verification, and evidence review.