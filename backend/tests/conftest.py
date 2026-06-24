import os
from pathlib import Path
import pytest

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db.database import Base, get_db
from app.db.models import Document, DocumentChunk, Claim

ENV_FILE = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(ENV_FILE)

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")
if not TEST_DATABASE_URL:
    raise RuntimeError(
        f"TEST_DATABASE_URL was not found. Add it to {ENV_FILE}."
    )

test_engine = create_engine(TEST_DATABASE_URL)
TestSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine
)
def override_get_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def reset_test_database():
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)

    yield

    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def db_session():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def sample_claim_with_chunk(db_session):
    db = db_session
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


@pytest.fixture
def sample_claim_without_evidence(db_session):
    db = db_session
    claim = Claim(
        claim_text = "zephyrion quantaflare lumicore",
        source_text="zephyrion quantaflare lumicore"
    )
    db.add(claim)
    db.commit()
    db.refresh(claim)
    yield claim

@pytest.fixture
def sample_claim_with_ranked_chunks(db_session):
    db = db_session

    document = Document(
        filename="ranked_chunks_test.pdf",
        file_type="pdf"
    )
    db.add(document)
    db.commit()
    db.refresh(document)

    high_score_chunk = DocumentChunk(
    document_id=document.id,
    page_number=1,
    chunk_index=0,
    content="nebula orbit quantum signal archive"
    )

    low_score_chunk = DocumentChunk(
    document_id=document.id,
    page_number=1,
    chunk_index=1,
    content="nebula orbit archive"
    )
    db.add(high_score_chunk)
    db.add(low_score_chunk)

    claim = Claim(
    claim_text="nebula orbit quantum signal",
    source_text="Ranked retrieval test source text."
    )
    db.add(claim)

    db.commit()
    db.refresh(high_score_chunk)
    db.refresh(low_score_chunk)
    db.refresh(claim)

    yield {
        "claim": claim,
        "high_score_chunk": high_score_chunk,
        "low_score_chunk": low_score_chunk
    }

    