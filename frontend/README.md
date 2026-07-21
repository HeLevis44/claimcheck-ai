# ClaimCheck AI Frontend

This is the Next.js frontend for ClaimCheck AI, a full-stack claim verification application. The frontend provides a polished dashboard for uploading source documents, creating claims, running verification, reviewing evidence, and inspecting detailed verification reports.

## Tech Stack

- Next.js App Router
- React
- TypeScript
- Tailwind CSS
- FastAPI backend integration

## Main Routes

```text
/
  Dashboard landing page with navigation to the main workflows.

/documents
  Upload PDFs, search uploaded documents, and paginate document results.

/claims
  Create claims, search claims, select verification mode, run verification, and review evidence.

/verification-results/[verificationId]
  Detailed verification report with result summary, confidence interpretation, evidence review, statistics, and metadata.
```

## Features

- Dashboard-style landing page
- PDF upload workflow
- Uploaded document list
- Document search and pagination
- Claim creation workflow
- Claim search and pagination
- Rule-based and OpenAI verification mode selection
- Latest verification result display
- Evidence chunk display with expand/collapse support
- Verification detail page
- Confidence progress display
- Status and confidence interpretation
- Evidence review with show/hide interaction
- Copy summary and copy evidence actions
- Shared reusable components for search, pagination, cards, and verification UI
- Loading, error, empty, disabled, and interactive states

## Frontend Structure

```text
src/
  app/
    page.tsx
    documents/
      page.tsx
    claims/
      page.tsx
    verification-results/
      [verificationId]/
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

## Component Roles

```text
app/page.tsx
  Provides the dashboard landing page and links to Documents and Claims.

app/documents/page.tsx
  Owns document workflow state and handles PDF upload, document search, and pagination.

app/claims/page.tsx
  Owns claim workflow state and handles claim creation, search, pagination, verification, and evidence retrieval.

app/verification-results/[verificationId]/page.tsx
  Owns verification detail state and renders a review-style report for one verification result.

components/
  Own reusable UI blocks. Components receive data and event handlers through props and do not directly call backend APIs.

lib/api.ts
  Centralizes frontend API requests to the FastAPI backend.

types/api.ts
  Defines TypeScript types for backend API responses.
```

## Local Development

Start the backend first from the project root or backend directory, then start the frontend:

```bash
cd ~/Desktop/claim_ai/frontend
npm run dev
```

Open:

```text
http://localhost:3000
```

The frontend expects the backend to run at:

```text
http://127.0.0.1:8000
```

You can override this with:

```bash
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
```

## Build Check

Run this before committing frontend changes:

```bash
cd ~/Desktop/claim_ai/frontend
npm run build
```

## Demo Flow

1. Open the dashboard at `http://localhost:3000`.
2. Go to the Documents page.
3. Upload a PDF.
4. Search uploaded documents.
5. Use Previous and Next pagination controls.
6. Return to the dashboard.
7. Go to the Claims page.
8. Create a claim.
9. Search claims.
10. Select a verification mode.
11. Verify a claim.
12. Review the latest verification result and evidence chunks.
13. Click `View detail`.
14. Review the detailed verification report.
15. Use the confidence bar, status summary, evidence review, copy buttons, and metadata section.
16. Return to the Claims page.

## Verification Detail Page

The verification detail page is designed as a review report rather than a basic database detail page. It includes:

- Dark hero section with confidence score
- Confidence progress bar
- Status badge and confidence badge
- Status interpretation
- Confidence interpretation
- Claim, evidence, and reasoning word-count statistics
- Selected evidence review
- Show/hide evidence text interaction
- Copy summary and copy evidence actions
- Technical metadata for debugging and traceability

## Status

The frontend is a polished MVP interface for the ClaimCheck AI backend. It supports the full local demo workflow: document upload, document search, document pagination, claim creation, claim search, verification, evidence review, and verification detail inspection.