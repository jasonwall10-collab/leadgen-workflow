#!/usr/bin/env python3
"""
Test Script for LeadGen Workflow
Simulates a complete workflow run from intake to pitch.
"""

import requests
import json
import time
from pathlib import Path

API_BASE = "http://localhost:8000/api"

def pretty_print(title, data):
    print(f"\n=== {title} ===")
    print(json.dumps(data, indent=2, ensure_ascii=False))

# 1. Intake
print("🔄 Starting workflow test...")
payload = {
    "name": "EcoClean Solutions",
    "location": "Adelaide, SA",
    "url": "https://ecocleansa.com.au"
}
resp = requests.post(f"{API_BASE}/intake", json=payload)
print("✅ Intake response:")
pretty_print("Intake Response", resp.json())

business_id = resp.json()["business_id"]
job_id = resp.json()["job_id"]
print(f"Business ID: {business_id}, Job ID: {job_id}")

# 2. Analysis
print("\n🔎 Running analysis...")
resp = requests.post(f"{API_BASE}/analyze", json={"business_id": business_id})
pretty_print("Analysis Response", resp.json())

# 3. Competitors
print("\n🏆 Running competitor analysis...")
resp = requests.post(f"{API_BASE}/competitors", json={"business_id": business_id})
pretty_print("Competitors Response", resp.json())

# 4. Rebuild
print("\n🏗️ Running rebuild...")
resp = requests.post(f"{API_BASE}/rebuild", json={"business_id": business_id})
pretty_print("Rebuild Response", resp.json())

# 5. Demo
print("\n🚀 Generating demo...")
resp = requests.post(f"{API_BASE}/demo", json={"business_id": business_id})
pretty_print("Demo Response", resp.json())

# 6. Pitch
print("\n📣 Generating pitch...")
resp = requests.post(f"{API_BASE}/pitch", json={"business_id": business_id})
pretty_print("Pitch Response", resp.json())

print("\n🎉 Workflow test completed!")