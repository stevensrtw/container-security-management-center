from pydantic import BaseModel
from typing import Any
from datetime import datetime

class SBOMUpload(BaseModel):
    name: str
    content: dict

class SBOMResponse(SBOMUpload):
    id: int
    uploaded_at: datetime

class ScanResultSchema(BaseModel):
    sbom_id: int
    results: dict

class ApprovalSchema(BaseModel):
    sbom_id: int
    approved: bool
    notes: Optional[str] = None

class TokenCreate(BaseModel):
    username: str
    role: str

class TokenResponse(BaseModel):
    token: str
    expires_at: datetime

class ScanResultSchema(BaseModel):
    id: int
    sbom_id: int
    results: Any
    cve_count: int
    high_count: int
    created_at: datetime

    class Config:
        orm_mode = True