from fastapi import APIRouter, Depends
from app.auth import get_current_user, require_role
from app.models import User

router = APIRouter()

@router.post("/push")
def push_to_emass():
    # Placeholder logic: connect to eMASS API, send results
    return {"status": "emass submission queued"}

@router.get("/me")
def whoami(current_user: User = Depends(get_current_user)):
    return {"username": current_user.username, "role": current_user.role}

@router.post("/admin-action")
def admin_only_action(current_user: User = Depends(require_role("admin"))):
    return {"message": "Only admins see this."}

@router.get("/me")
def whoami(current_user: User = Depends(get_current_user)):
    return {"username": current_user.username, "role": current_user.role}