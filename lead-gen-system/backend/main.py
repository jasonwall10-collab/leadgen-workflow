from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, List, Dict
import sqlite3
import json

app = FastAPI(title="LeadGenWorkflow API")
DB_PATH = "data/leads.db"

def get_conn():
    return sqlite3.connect(DB_PATH)

class Intake(BaseModel):
    name: str
    location: str
    url: Optional[str] = None

class Analyze(BaseModel):
    business_id: int
    page_content: Optional[str] = None

class CompetitorsReq(BaseModel):
    business_id: int

class Rebuild(BaseModel):
    business_id: int
    audit: Dict
    competitors: List[Dict]

class Demo(BaseModel):
    business_id: int
    rebuild_json: Dict

class Pitch(BaseModel):
    business_id: int
    rebuild_json: Dict
    demo_json: Dict

@app.post("/api/intake")
def intake(data: Intake):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO businesses (name, location, website_url, status) VALUES (?,?,?, 'pending')",
                (data.name, data.location, data.url))
    bid = cur.lastrowid
    conn.commit()
    conn.close()
    return {"business_id": bid, "status": "accepted"}

@app.post("/api/analyze")
def analyze(payload: Analyze):
    # placeholder analysis result
    audit = {
        "scores": {"design": 78, "seo": 72, "conversion": 65, "trust": 70, "mobile": 80},
        "finding_summary": "Initial audit performed. Key opportunities identified.",
        "quick_wins": ["Improve H1 clarity", "Add meta description", "Strengthen CTA contrast"],
        "weaknesses": ["No alt text on hero image", "Missing structured data"]
    }
    return {"audit": audit}

@app.post("/api/competitors")
def competitors(payload: CompetitorsReq):
    top3 = [
        {"name": "Local Pro Plumbing", "structure_strengths": ["Clear service pages"], "messaging_gaps": ["Unique value prop"]},
        {"name": "Adelaide Coffee Co", "structure_strengths": ["Strong about page"], "messaging_gaps": ["Pricing transparency"]},
        {"name": "Gym Pro Fitness", "structure_strengths": ["Conversion-optimized CTAs"], "messaging_gaps": ["Social proof"]},
    ]
    return {"top3": top3}

@app.post("/api/rebuild")
def rebuild(payload: Rebuild):
    rebuild_json = {
        "structure": ["Home", "About", "Services", "Pricing", "Contact"],
        "headings": ["Best Plumbing in Town", "Quality Coffee Nearby", "Fitness That Fits Your Schedule"],
        "CTAs": ["Get a Quote", "Book a Free Consultation"],
        "trust_signals": ["Testimonials", "Accreditations"]
    }
    return {"rebuild_json": rebuild_json}

@app.post("/api/demo")
def demo(payload: Demo):
    return {"demo_url": "http://localhost:8000/demos/placeholder"}

@app.post("/api/pitch")
def pitch(payload: Pitch):
    return {
        "executive_summary": "A concise executive summary for the lead.",
        "revenue_opportunity": "$24k/mo potential",
        "before_after": "Before: fragmented content; After: cohesive, conversion-focused site",
        "outbound_email": "Hi ..., we'd love to help...",
        "followup_email": "Just checking in..."
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
