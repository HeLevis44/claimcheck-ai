from app.db.models import VerificationResult
from app.schemas.verification import (
    ClaimSummaryResponse,
    EvidenceDetailResponse,
    VerificationDetailResponse,
    VerificationSummaryResponse,
)

def build_verification_detail_response(verification_result: VerificationResult,) -> VerificationDetailResponse:
    claim = verification_result.claim
    evidence_chunk = verification_result.evidence_chunk

    verification_summary = VerificationSummaryResponse(
        id=verification_result.id,
        status=verification_result.status,
        confidence=verification_result.confidence,
        reasoning=verification_result.reasoning,
        created_at=verification_result.created_at,
    )

    claim_summary = ClaimSummaryResponse(
        id = claim.id,
        claim_text = claim.claim_text,
        source_text = claim.source_text
    )

    evidence_detail = None

    if evidence_chunk is not None:
        evidence_detail = EvidenceDetailResponse(
            id=evidence_chunk.id,
            document_id=evidence_chunk.document_id,
            filename=evidence_chunk.document.filename,
            page_number=evidence_chunk.page_number,
            chunk_index=evidence_chunk.chunk_index,
            content=evidence_chunk.content,
        )

    return VerificationDetailResponse(
        verification=verification_summary,
        claim=claim_summary,
        evidence=evidence_detail,
    )