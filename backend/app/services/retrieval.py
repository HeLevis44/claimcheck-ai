import re
from app.db.models import DocumentChunk
from app.schemas.evidence import EvidenceResponse
STOP_WORDS = {
    "the", "and", "for", "with", "that", "this", "are", "was", "were",
    "from", "into", "has", "have", "had", "not", "but", "about",
    "than", "then", "they", "their", "there", "which", "when", "where",
    "what", "who", "why", "how", "can", "may", "might", "will",
    "would", "could", "should", "a", "an", "of", "to", "in", "on", "by", "is", "it", "as", "at", "or"
}


def extract_keywords(text: str) -> list[str]:
    cleaned_text = re.sub(r"[^a-zA-Z0-9\s]", " ", text.lower())
    words = cleaned_text.split()
    return [word for word in words if len(word) >= 3 and word not in STOP_WORDS]

def retrieve_evidence_for_claim(claim, db):
    key_words = extract_keywords(claim.claim_text)
    if not key_words:
        return []
    
    evidence_list = []
    chunk_scores = {}

    for keyword in key_words:
        chunks = db.query(DocumentChunk).filter(DocumentChunk.content.ilike(f"%{keyword}%")).all()
        for chunk in chunks:
            if chunk.id not in chunk_scores:
                chunk_scores[chunk.id] = {
                    "chunk": chunk,
                    "score": 0
                }
            chunk_scores[chunk.id]["score"] += 1
    sorted_chunks = sorted(chunk_scores.values(), key=lambda x: x["score"], reverse=True)
    for chunk_info in sorted_chunks[:10]:
        chunk = chunk_info["chunk"]
        evidence_list.append(EvidenceResponse(
            chunk_id=chunk.id,
            document_id=chunk.document_id,
            page_number=chunk.page_number,
            chunk_index=chunk.chunk_index,
            content=chunk.content,
            score=chunk_info["score"]
        ))
    return evidence_list