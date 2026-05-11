from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
import os, shutil, uuid, time, json
from datetime import datetime

APP_START_TIME = time.time()

app = FastAPI(title="NaviSearch AI Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

SYSTEM_LOGS = []

class UserCorrection(BaseModel):
    tablet_id: str
    sign_id: str
    proposed_glyph: str
    user_comment: Optional[str] = None

def add_log(event, status="ok", details=None):
    item = {
        "time": datetime.now().isoformat(timespec="seconds"),
        "event": event,
        "status": status,
        "details": details or {}
    }
    SYSTEM_LOGS.append(item)
    if len(SYSTEM_LOGS) > 100:
        SYSTEM_LOGS.pop(0)

@app.get("/")
def home():
    return {
        "status": "online",
        "backend_version": "1.5",
        "system": "NaviSearch AI Backend",
        "module": "ADS Tablet Reader",
        "processor": "Navi_Brat_Hybrid_v1",
        "bridge": "BRAT_ACTIVE",
        "mode": "ngrok_test",
        "uptime_seconds": int(time.time() - APP_START_TIME),
        "timestamp": datetime.now().isoformat(timespec="seconds")
    }

@app.get("/api/v1/logs")
def get_logs():
    return {"status": "ok", "count": len(SYSTEM_LOGS[-50:]), "logs": SYSTEM_LOGS[-50:]}

@app.post("/api/v1/tablet/upload")
async def upload_tablet(file: UploadFile = File(...)):
    try:
        allowed = ["image/jpeg", "image/png", "image/webp"]
        if file.content_type not in allowed:
            raise HTTPException(status_code=400, detail="INVALID_FORMAT: Only JPG, PNG and WebP are supported.")

        tablet_id = f"ADS-{uuid.uuid4().hex[:8].upper()}"
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_name = file.filename.replace(" ", "_")
        filename = f"{timestamp}_{safe_name}"
        filepath = os.path.join(UPLOAD_DIR, filename)

        with open(filepath, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        result = {
            "status": "uploaded",
            "tablet_id": tablet_id,
            "filename": filename,
            "path": filepath,
            "ads_payload": {
                "id": tablet_id,
                "status": "PROPOSED",
                "metadata": {
                    "filename": file.filename,
                    "content_type": file.content_type,
                    "processor": "Navi_Brat_Hybrid_v1",
                    "source": "user_upload"
                },
                "detections": [],
                "ads_structure": {
                    "raw_transliteration": "",
                    "confidence_score": 0.0,
                    "interpretation_layer": "pending",
                    "reading": "Pending analysis"
                },
                "user_correction": None,
                "warning": "Automated analysis. Verification required."
            }
        }

        add_log("tablet_upload", "ok", result)
        return result

    except Exception as e:
        error = {"status": "error", "message": str(e)}
        add_log("tablet_upload", "error", error)
        return JSONResponse(status_code=200, content=error)

@app.post("/api/v1/tablet/analyze")
def analyze_tablet():
    result = {
        "status": "PROPOSED",
        "system": "ADS Tablet Reader",
        "version": "1.5",
        "processor": "Navi_Brat_Hybrid_v1",
        "bridge": "BRAT_SYNC_OK",
        "user_correction": None,
        "detections": [
            {"sign_id": "S1", "glyph": "wedge_cluster_A", "confidence": 0.32, "bbox": [80, 60, 140, 120]},
            {"sign_id": "S2", "glyph": "wedge_cluster_B", "confidence": 0.28, "bbox": [170, 75, 230, 135]}
        ],
        "ads_structure": {
            "record_type": "PROPOSED",
            "schema": "RECORD + SUMMARY + META",
            "raw_transliteration": "o-r-o-r-a-m",
            "confidence_score": 0.85,
            "interpretation_layer": "ADS_initial_scan",
            "reading": "Possible structured record / early ADS scan"
        },
        "warning": "Automated analysis. Verification required."
    }

    add_log("tablet_analyze", "ok", result)
    return result

@app.post("/api/v1/correction")
async def save_correction(correction: UserCorrection):
    try:
        log_entry = {
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "data": correction.dict()
        }

        path = os.path.join(UPLOAD_DIR, "corrections.log")
        with open(path, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")

        add_log("user_correction", "ok", log_entry)

        return {
            "status": "SAVED",
            "message": "Correction saved as training data",
            "correction": log_entry
        }

    except Exception as e:
        error = {"status": "error", "message": str(e)}
        add_log("user_correction", "error", error)
        return JSONResponse(status_code=200, content=error)

@app.get("/api/v1/bridge")
def bridge_test():
    return {
        "status": "ONLINE",
        "bridge": "BRAT_ACTIVE",
        "message": "Direct bridge operational"
    }

@app.options("/{full_path:path}")
async def options_handler(full_path: str):
    return {"status": "ok"}