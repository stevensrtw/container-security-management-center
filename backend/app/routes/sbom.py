from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.auth import get_current_user, require_role
from app.models import SBOM, User
from app.schemas import SBOMUpload, SBOMResponse
from typing import List

router = APIRouter()

@router.post("/upload", response_model=SBOMResponse)
def upload_sbom(sbom: SBOMUpload):
    db: Session = SessionLocal()
    db_sbom = SBOM(name=sbom.name, content=sbom.content)
    db.add(db_sbom)
    db.commit()
    db.refresh(db_sbom)
    return db_sbom

@router.get("/list", response_model=List[SBOMResponse])
def list_sboms():
    db: Session = SessionLocal()
    return db.query(SBOM).all()

@router.get("/me")
def whoami(current_user: User = Depends(get_current_user)):
    return {"username": current_user.username, "role": current_user.role}

@router.post("/admin-action")
def admin_only_action(current_user: User = Depends(require_role("admin"))):
    return {"message": "Only admins see this."}