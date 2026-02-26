import os
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import sqlite3
from datetime import datetime
from typing import Optional, List, Dict, Any
import json
from pathlib import Path

# ======================
# Configuration
# ======================
BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / "data" / "leads.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# Telegram config
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

# ======================
# FastAPI app
# ======================
app = FastAPI(title="LeadGen Workflow API")

# CORS (frontend will be on different port in dev, but in Coolify both will share domain)
app.add_middleware(
    cors_middleware := CORSMiddleware,
    allow_origins=["*"],  # In production lock this down
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ======================
# Database helpers
# ======================
def get_conn():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_conn()
    cur = conn.cursor()
    try:
        # Businesses
        cur.execute('''
            CREATE TABLE IF NOT EXISTS businesses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                location TEXT,
                website_url TEXT,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        # Jobs (state machine)
        cur.execute('''
            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                business_id INTEGER,
                stage TEXT NOT NULL,
                status TEXT DEFAULT 'idle',
                data_json TEXT,
                last_error TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (business_id) REFERENCES businesses(id)
            )
        ''')
        # Campaign/Stage definitions (you can expand)
        cur.execute('''
            CREATE TABLE IF NOT EXISTS stages (
                stage_name TEXT PRIMARY KEY,
                description TEXT
            )
        ''')
        # Insert default stages
        stages = [
            ("Intake", "Collect business info"),
            ("Analysis", "Website audit"),
            ("Competitors", "Top competitor research"),
            ("Rebuild", "Generate new structure"),
            ("Demo", "Deploy demo site"),
            ("Pitch", "Generate pitch materials")
        ]
        cur.executemany("INSERT OR IGNORE INTO stages (stage_name, description) VALUES (?,?)", stages)
        cur.execute('''
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                job_id INTEGER,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                level TEXT,
                message TEXT,
                FOREIGN KEY (job_id) REFERENCES jobs(id)
            )
        ''')
    except Exception as e:
        print(f"DB init error: {e}")
    finally:
        conn.commit()
        conn.close()

def log_job_event(job_id: int, level: str, message: str):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO logs (job_id, level, message) VALUES (?,?,?)", (job_id, level, message))
    conn.commit()
    conn.close()

# ======================
# Pydantic models (input validation)
# ======================
class Intake(BaseModel):
    name: str
    location: str
    url: Optional[str] = None

class Analyze(BaseModel):
    business_id: int

class Competitors(BaseModel):
    business_id: int

class Rebuild(BaseModel):
    business_id: int

class Demo(BaseModel):
    business_id: int

class Pitch(BaseModel):
    business_id: int

# ======================
# Helper functions
# ======================
def get_business_id(name: str, location: str) -> Optional[int]:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id FROM businesses WHERE name=? AND location=?", (name, location))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else None

def create_job(business_id: int, stage: str):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO jobs (business_id, stage) VALUES (?,?)",
        (business_id, stage)
    )
    job_id = cur.lastrowid
    conn.commit()
    conn.close()
    return job_id

def get_next_stage(stage: str) -> Optional[str]:
    # simple sequential flow
    stages = ["Intake", "Analysis", "Competitors", "Rebuild", "Demo", "Pitch"]
    idx = stages.index(stage) if stage in stages else -1
    return stages[idx + 1] if idx + 1 < len(stages) else None

def update_job_stage(job_id: int, new_stage: str, data_json: str = None, status: str = "processing"):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("UPDATE jobs SET stage=?, status=?, data_json=? WHERE id=?", (new_stage, status, data_json, job_id))
    conn.commit()
    conn.close()

def get_job_by_business(business_id: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM jobs WHERE business_id=?", (business_id,))
    rows = cur.fetchall()
    conn.close()
    return rows[0] if rows else None

# ======================
# Mock processing functions (replace with real implementations)
# ======================
def mock_analysis(audit_data: Dict) -> Dict:
    # Return a simple audit result that conforms to schema_audit.json
    return {
        "scores": {
            "design": 78,
            "seo": 72,
            "conversion": 65,
            "trust": 70,
            "mobile": 80
        },
        "finding_summary": "Initial audit completed.",
        "quick_wins": ["Clear navigation", "Responsive layout"],
        "weaknesses": ["Missing alt text", "No structured data"]
    }

def mock_competitors_analysis() -> Dict:
    return {
        "top3": [
            {"name": "Local Pro Plumbing", "structure_strengths": ["Clear service pages"], "messaging_gaps": ["Unique value prop"]},
            {"name": "Adelaide Coffee Co", "structure_strengths": ["Strong about page"], "messaging_gaps": ["Pricing transparency"]},
            {"name": "Gym Pro Fitness", "structure_strengths": ["Conversion-optimized CTAs"], "messaging_gaps": ["Social proof"]},
        ]
    }

def mock_rebuild_output() -> Dict:
    return {
        "structure": ["Home", "About", "Services", "Pricing", "Contact"],
        "headings": ["Best Plumbing in Town", "Quality Coffee Nearby", "Fitness That Fits Your Schedule"],
        "CTAs": ["Get a Quote", "Book a Free Consultation"],
        "trust_signals": ["Testimonials", "Accreditations"]
    }

def mock_demo_url() -> Dict:
    return {"demo_url": "http://localhost:8000/demos/placeholder"}

def mock_pitch_output() -> Dict:
    return {
        "executive_summary": "Executive summary for the lead.",
        "revenue_opportunity": "$24k/month potential",
        "before_after": "Before: fragmented; After: cohesive conversion‑focused site",
        "outbound_email": "Hi … we’d love to help …",
        "followup_email": "Just checking in …"
    }

def send_telegram(message: str):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        return
    import httpx
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    try:
        httpx.post(url, json=payload, timeout=5.0)
    except Exception as e:
        print(f"Telegram send error: {e}")

# ======================
# App lifecycle
# ======================

@app.on_event("startup")
def _startup():
    # Ensure DB schema exists before any request handlers run
    init_db()

# ======================
# API Endpoints
# ======================

@app.post("/api/intake")
async def intake(payload: Intake):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO businesses (name, location, website_url, status) VALUES (?,?,?, 'pending')",
        (payload.name, payload.location, payload.url)
    )
    business_id = cur.lastrowid
    conn.commit()
    conn.close()

    job_id = create_job(business_id=business_id, stage="Intake")
    # Auto transition to next stage (Analysis)
    next_stage = get_next_stage("Intake")
    update_job_stage(job_id, next_stage, status="processing")
    return {"business_id": business_id, "job_id": job_id, "status": "accepted"}

@app.post("/api/analyze")
async def analyze(payload: Analyze):
    job = get_job_by_business(payload.business_id)
    if not job or job[2] != "Analysis":  # stage index 1 in our flow
        raise HTTPException(status_code=400, detail="Job not in Analysis stage")
    # Collect audit output (placeholder)
    audit = mock_analysis({"dummy": "data"})
    update_job_stage(job_id=job[0], new_stage=get_next_stage("Analysis"), data_json=json.dumps(audit))
    send_telegram(f"🔎 Analysis complete for business {payload.business_id}")
    return {"audit": audit}

@app.post("/api/competitors")
async def competitors(payload: Competitors):
    job = get_job_by_business(payload.business_id)
    if not job or job[2] != "Competitors":
        raise HTTPException(status_code=400, detail="Job not in Competitors stage")
    comps = mock_competitors_analysis()
    update_job_stage(job_id=job[0], new_stage=get_next_stage("Competitors"), data_json=json.dumps(comps))
    send_telegram(f"🔎 Competitors analysis done for business {payload.business_id}")
    return {"top3": comps["top3"]}

@app.post("/api/rebuild")
async def rebuild(payload: Rebuild):
    job = get_job_by_business(payload.business_id)
    if not job or job[2] != "Rebuild":
        raise HTTPException(status_code=400, detail="Job not in Rebuild stage")
    rebuild = mock_rebuild_output()
    update_job_stage(job_id=job[0], new_stage=get_next_stage("Rebuild"), data_json=json.dumps(rebuild))
    send_telegram(f"🏗️ Rebuild completed for business {payload.business_id}")
    return {"rebuild": rebuild}

@app.post("/api/demo")
async def demo(payload: Demo):
    job = get_job_by_business(payload.business_id)
    if not job or job[2] != "Demo":
        raise HTTPException(status_code=400, detail="Job not in Demo stage")
    demo = mock_demo_url()
    update_job_stage(job_id=job[0], new_stage=get_next_stage("Demo"), data_json=json.dumps(demo))
    send_telegram(f"🚀 Demo deployed for business {payload.business_id}")
    return demo

@app.post("/api/pitch")
async def pitch(payload: Pitch):
    job = get_job_by_business(payload.business_id)
    if not job or job[2] != "Pitch":
        raise HTTPException(status_code=400, detail="Job not in Pitch stage")
    pitch = mock_pitch_output()
    update_job_stage(job_id=job[0], new_stage="Pitch", data_json=json.dumps(pitch), status="completed")
    send_telegram(f"📣 Pitch generated for business {payload.business_id}")
    return pitch

@app.post("/api/upload-csv")
async def upload_csv(file: UploadFile = File(...)):
    # Save CSV to uploads dir
    save_path = UPLOAD_DIR / file.filename
    contents = await file.read()
    with open(save_path, "wb") as f:
        f.write(contents)

    # Very simple CSV import: assumes header row with name,location,url
    import csv, io
    try:
        stream = io.StringIO(contents.decode("utf-8"))
        reader = csv.DictReader(stream)
        for row in reader:
            name = row.get("name")
            location = row.get("location")
            url = row.get("website_url", "")
            if name and location:
                conn = get_conn()
                cur = conn.cursor()
                cur.execute(
                    "INSERT INTO businesses (name, location, website_url, status) VALUES (?,?,?, 'pending')",
                    (name, location, url)
                )
                conn.commit()
                conn.close()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"CSV import error: {e}")

    return {"detail": "CSV file saved, data appended to businesses table."}

@app.get("/api/status/{job_id}")
async def status(job_id: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT stage, status, data_json FROM jobs WHERE id=?", (job_id,))
    row = cur.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Job not found")
    return {"job_id": job_id, "stage": row[0], "status": row[1], "data": row[2]}

@app.get("/api/business/{business_id}")
async def business(business_id: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT name, location, website_url FROM businesses WHERE id=?", (business_id,))
    row = cur.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Business not found")
    return {"name": row[0], "location": row[1], "website_url": row[2]}

@app.get("/")
async def root():
    return {"message": "LeadGen Workflow API – use /docs for Swagger UI"}

if __name__ == "__main__":
    init_db()
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=False)