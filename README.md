# ClaimCheck AI

ClaimCheck AI is a full-stack AI-powered verification platform that checks whether claims in generated writing are supported by uploaded source documents.

Users can upload source PDFs, paste AI-generated text, and receive claim-level verification results with supporting evidence from the original documents.

## Problem

AI-generated writing often contains unsupported claims, misleading citations, or fabricated references. Even when a source is provided, the cited document may not actually support the claim.

ClaimCheck AI helps users verify generated content by grounding each claim in uploaded source documents.

## Core Features

- Upload source PDF documents
- Parse and chunk document text with page-level metadata
- Paste AI-generated writing for verification
- Automatically extract checkable claims
- Retrieve relevant evidence from uploaded documents
- Classify each claim as:
  - Supported
  - Partially supported
  - Unsupported
  - Not enough evidence
- Display evidence with document name and page number

## Tech Stack

### Frontend
- Next.js
- TypeScript
- Tailwind CSS

### Backend
- FastAPI
- Python
- PostgreSQL
- pgvector
- PyMuPDF

### AI
- Embeddings for document retrieval
- LLM-based claim extraction and verification
- Structured JSON outputs

### DevOps
- Docker
- Docker Compose
- Environment variables
- API testing

## System Architecture

```text
User
  |
  v
Next.js Frontend
  |
  v
FastAPI Backend
  |
  +--> PDF Parser
  |
  +--> PostgreSQL + pgvector
  |
  +--> LLM API
  |
  v
Verification Report


MVP Workflow

1. User uploads one or more PDF documents.
2. Backend parses the PDFs into page-level text chunks.
3. Chunks are stored in PostgreSQL with vector embeddings.
4. User pastes AI-generated writing.
5. The system extracts individual claims.
6. Each claim is matched against relevant document chunks.
7. The system determines whether the evidence supports the claim.
8. Results are displayed in a claim-level dashboard.

Planned Milestones

Phase 1: Project Setup

* Initialize frontend and backend apps
* Set up Docker Compose
* Create PostgreSQL database
* Add basic API health check

Phase 2: Document Ingestion

* Upload PDFs
* Parse PDF text
* Split text into chunks
* Store chunks with document metadata

Phase 3: Retrieval

* Generate embeddings
* Store vectors with pgvector
* Retrieve top-k evidence chunks for each claim

Phase 4: Claim Verification

* Extract claims from generated writing
* Classify claim support level using retrieved evidence
* Return structured verification results

Phase 5: Frontend Dashboard

* Upload interface
* Text input interface
* Claim result table
* Expandable evidence viewer

Local Development

Coming soon.

Status

This project is currently under active development.