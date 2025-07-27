from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import ScanResult, SBOM, ScanRetry
from app.schemas import ScanResultSchema
from datetime import datetime, timedelta
from app.utils.trivy_runner import run_trivy_scan
from app.auth import get_current_user, require_role

router = APIRouter()

@router.post("/submit", response_model=ScanResultSchema)
def submit_scan(scan: ScanResultSchema):
    db: Session = SessionLocal()
    sbom = db.query(SBOM).filter(SBOM.id == scan.sbom_id).first()
    if not sbom:
        raise HTTPException(statfrom app.utils.trivy_runner import run_trivy_scan
us_code=404, detail="SBOM not found")
    db_scan = ScanResult(sbom_id=scan.sbom_id, results=scan.results, created_at=datetime.utcnow())
    db.add(db_scan)
    db.commit()
    db.refresh(db_scan)
    return scan

@router.get("/results/{sbom_id}")
def get_all_results(sbom_id: int):
    db: Session = SessionLocal()
    return db.query(ScanResult).filter(ScanResult.sbom_id == sbom_id).order_by(ScanResult.created_at.desc()).all()

@router.get("/scans/latest")
def get_latest_scan(sbom_id: int):
    db: Session = SessionLocal()
    scan = db.query(ScanResult).filter(ScanResult.sbom_id == sbom_id).order_by(ScanResult.created_at.desc()).first()
    if not scan:
        raise HTTPException(status_code=404, detail="No scan found")
    return scan

@router.post("/retry")
def retry_scan(sbom_id: int, request: Request):
    db = SessionLocal()
    user = request.headers.get("X-User", "anonymous")

    # Check SBOM exists
    sbom = db.query(SBOM).filter(SBOM.id == sbom_id).first()
    if not sbom:
        raise HTTPException(status_code=404, detail="SBOM not found")

    # Check retry count
    retry_count = db.query(ScanRetry).filter(ScanRetry.sbom_id == sbom_id).count()
    if retry_count >= 3:
        raise HTTPException(status_code=429, detail="Retry limit reached")

    # Check cooldown
    last_retry = (
        db.query(ScanRetry)
        .filter(ScanRetry.sbom_id == sbom_id)
        .order_by(ScanRetry.timestamp.desc())
        .first()
    )
    if last_retry and (datetime.utcnow() - last_retry.timestamp) < timedelta(minutes=5):
        raise HTTPException(status_code=429, detail="Retry cooldown in effect. Try again later.")

    # Run Trivy scan on SBOM content
    try:
        scan_result_json = run_trivy_scan(sbom.content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # Save scan result
    db_scan = ScanResult(
        sbom_id=sbom.id,
        results=scan_result_json,
        created_at=datetime.utcnow()
    )
    db.add(db_scan)

    # Log retry
    db_retry = ScanRetry(
        sbom_id=sbom.id,
        requested_by=user,
        timestamp=datetime.utcnow()
    )
    db.add(db_retry)

    db.commit()

    return {"status": "scan complete", "result_id": db_scan.id}

@router.get("/me")
def whoami(current_user: User = Depends(get_current_user)):
    return {"username": current_user.username, "role": current_user.role}

@router.post("/admin-action")
def admin_only_action(current_user: User = Depends(require_role("admin"))):
    return {"message": "Only admins see this."}