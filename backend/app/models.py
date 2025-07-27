from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, JSON, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base
from typing import Any
from pydantic import BaseModel

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    role = Column(String)
    email = Column(String, unique=True)

class SBOM(Base):
    __tablename__ = "sboms"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    content = Column(JSON)
    uploaded_at = Column(DateTime, default=datetime.utcnow)

class ScanResult(Base):
    __tablename__ = "scan_results"
    id = Column(Integer, primary_key=True, index=True)
    sbom_id = Column(Integer, ForeignKey("sboms.id"))
    results = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

class Approval(Base):
    __tablename__ = "approvals"
    id = Column(Integer, primary_key=True, index=True)
    sbom_id = Column(Integer, ForeignKey("sboms.id"))
    approved_by = Column(Integer, ForeignKey("users.id"))
    approved = Column(Boolean)
    notes = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

class Token(Base):
    __tablename__ = "tokens"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    token = Column(String)
    expires_at = Column(DateTime)

class ScanResult(Base):
    __tablename__ = "scan_results"
    id = Column(Integer, primary_key=True, index=True)
    sbom_id = Column(Integer, ForeignKey("sboms.id"))
    results = Column(JSON)
    cve_count = Column(Integer, default=0)
    high_count = Column(Integer, default=0)
    created_at = Column(DateTime)
    sbom = relationship("SBOM", back_populates="scan_results")