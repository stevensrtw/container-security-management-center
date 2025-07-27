# backend/app/utils/trivy_runner.py

import subprocess
import tempfile
import json

def run_trivy_scan(sbom_content: str) -> dict:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as sbom_file:
        sbom_file.write(sbom_content.encode("utf-8"))
        sbom_file.flush()

        try:
            result = subprocess.run(
                ["trivy", "sbom", "--format", "json", sbom_file.name],
                capture_output=True,
                text=True,
                check=True
            )
            return json.loads(result.stdout)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Trivy scan failed: {e.stderr}")
