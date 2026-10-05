from fastapi import FastAPI
from fastapi.responses import FileResponse
from pathlib import Path
import json

app = FastAPI(
    title="CloudDefend API",
    description="Cloud Security Monitoring and Threat Detection API",
    version="1.0.0"
)

BASE_DIR = Path("/home/azureuser/clouddefend")
ALERT_FILE = BASE_DIR / "logs" / "alerts.json"
DASHBOARD_FILE = BASE_DIR / "dashboard.html"


@app.get("/")
def dashboard():
    return FileResponse(DASHBOARD_FILE)


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/alerts")
def get_alerts():
    try:
        return json.loads(ALERT_FILE.read_text())
    except Exception:
        return []


@app.get("/stats")
def stats():
    alerts = get_alerts()

    return {
        "total_alerts": len(alerts),
        "high_severity": sum(
            1 for a in alerts
            if a.get("severity") == "HIGH"
        )
    }
