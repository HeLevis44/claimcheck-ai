from app.db.database import Base
from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
import datetime

class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True, nullable=False)
    file_type = Column(String,nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    chunks = relationship("DocumentChunk", back_populates="document")

class DocumentChunk(Base):
    __tablename__ = 'document_chunks'
    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey('documents.id'),nullable=False)
    page_number = Column(Integer, nullable=False)
    chunk_index = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    document = relationship("Document", back_populates="chunks")
    verification_results = relationship("VerificationResult", back_populates="evidence_chunk")

class Claim(Base):
    __tablename__ = 'claims'
    id = Column(Integer, primary_key=True, index=True)
    claim_text = Column(Text, nullable=False)
    source_text = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    verification_results = relationship("VerificationResult", back_populates="claim")

class VerificationResult(Base):
    __tablename__ = 'verification_results'
    id = Column(Integer, primary_key=True, index=True)
    claim_id = Column(Integer, ForeignKey('claims.id'), nullable=False)
    evidence_chunk_id = Column(Integer, ForeignKey('document_chunks.id'), nullable=True)
    status = Column(String, nullable=False)
    confidence = Column(Float, nullable=False)
    reasoning = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    claim = relationship("Claim", back_populates="verification_results")
    evidence_chunk = relationship("DocumentChunk", back_populates="verification_results")