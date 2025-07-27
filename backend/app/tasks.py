from .celery_worker import celery_app
from .utils.trivy_runner import run_trivy_scan
from .database import SessionLocal
from .models import SBOM, ScanResult, ScanRetry
from datetime import datetime

@celery_app.task
def run_trivy_scan_task(sbom_id: int, requested_by: str = "system"):
    db = SessionLocal()
    sbom = db.query(SBOM).filter(SBOM.id == sbom_id).first()
    if not sbom:
        return {"error": "SBOM not found"}

    try:
        scan_result = run_trivy_scan(sbom.content)
    except Exception as e:
        return {"error": str(e)}

    db_scan = ScanResult(
        sbom_id=sbom.id,
        results=scan_result,
        cve_count=len(scan_result.get("Results", [])),
        high_count=sum(1 for r in scan_result.get("Results", []) if any(v["Severity"] == "HIGH" for v in r.get("Vulnerabilities", []))),
        created_at=datetime.utcnow()
    )
    db.add(db_scan)

    db_retry = ScanRetry(sbom_id=sbom.id, requested_by=requested_by, timestamp=datetime.utcnow())
    db.add(db_retry)

    db.commit()
    return {"status": "complete", "sbom_id": sbom.id}
