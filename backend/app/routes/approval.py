from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db  # add this to your database module
from app.models import Approval, SBOM, User
from app.auth import get_current_user, require_role
from app.schemas import ApprovalSchema
from datetime import datetime

router = APIRouter()

@router.post("/submit")
def submit_approval(data: ApprovalSchema, db: Session = Depends(get_db)):
    sbom = db.query(SBOM).filter(SBOM.id == data.sbom_id).first()
    if not sbom:
        raise HTTPException(status_code=404, detail="SBOM not found")
    
    approval = Approval(
        sbom_id=data.sbom_id,
        approved=data.approved,
        notes=data.notes,
        timestamp=datetime.utcnow()
    )
    db.add(approval)
    db.commit()
    return {"status": "submitted"}

@router.get("/list")
def list_approvals(db: Session = Depends(get_db)):
    return db.query(Approval).order_by(Approval.timestamp.desc()).all()

@router.get("/me")
def whoami(current_user: User = Depends(get_current_user)):
    return {"username": current_user.username, "role": current_user.role}

@router.post("/admin-action")
def admin_only_action(current_user: User = Depends(require_role("admin"))):
    return {"message": "Only admins see this."}