import pytest

from app.db.database import SessionLocal
from app.db.models import Document, DocumentChunk, Claim

@pytest.fixture
def sample_claim_with_chunk():
    db = SessionLocal()

    document = Document(
        filename = "test_document.pdf",
        file_type="pdf"
    )
    db.add(document)
    db.commit()
    db.refresh(document)

    chunk = DocumentChunk(
        document_id = document.id,
        page_number=1,
        chunk_index=0,
        content="orion_spectral_zenith_314159"
    )
    db.add(chunk)

    claim = Claim(
        claim_text="orion_spectral_zenith_314159",
        source_text="Test source text."
    )
    db.add(claim)

    db.commit()
    db.refresh(chunk)
    db.refresh(claim)

    yield{
        "claim":claim,
        "chunk":chunk
    }

    db.close()

@pytest.fixture
def sample_claim_without_evidence():
    db = SessionLocal()
    claim = Claim(
        claim_text = "zephyrion quantaflare lumicore",
        source_text="zephyrion quantaflare lumicore"
    )
    db.add(claim)
    db.commit()
    db.refresh(claim)
    yield claim
    db.close()