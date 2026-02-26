from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict
import json
from datetime import datetime

# ======================
# Intake Models
# ======================
class IntakeRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    location: str = Field(..., min_length=1, max_length=200)
    url: Optional[str] = Field(None, max_length=500)

    @validator('url')
    def validate_url(cls, v):
        if v and not v.startswith(('http://', 'https://')):
            raise ValueError('URL must start with http:// or https://')
        return v

class IntakeResponse(BaseModel):
    business_id: int
    job_id: int
    status: str  # accepted | requires_url_discovery

# ======================
# Analysis Models
# ======================
class AnalysisRequest(BaseModel):
    business_id: int

class AuditScore(BaseModel):
    design: int = Field(..., ge=0, le=100)
    seo: int = Field(..., ge=0, le=100)
    conversion: int = Field(..., ge=0, le=100)
    trust: int = Field(..., ge=0, le=100)
    mobile: int = Field(..., ge=0, le=100)

class AuditResult(BaseModel):
    scores: AuditScore
    finding_summary: str = Field(..., max_length=2000)
    quick_wins: List[str] = Field(default_factory=list, max_items=10)
    weaknesses: List[str] = Field(default_factory=list, max_items=10)

class AnalysisResponse(BaseModel):
    business_id: int
    audit: AuditResult

# ======================
# Competitors Models
# ======================
class CompetitorInfo(BaseModel):
    name: str = Field(..., max_length=200)
    structure_strengths: List[str] = Field(default_factory=list, max_items=5)
    messaging_gaps: List[str] = Field(default_factory=list, max_items=5)

class CompetitorsRequest(BaseModel):
    business_id: int

class CompetitorsResponse(BaseModel):
    business_id: int
    top3: List[CompetitorInfo]

# ======================
# Rebuild Models
# ======================
class RebuildRequest(BaseModel):
    business_id: int
    audit: AuditResult
    competitors: List[CompetitorInfo]

class RebuildOutput(BaseModel):
    structure: List[str] = Field(default_factory=list, max_items=20)
    headings: List[str] = Field(default_factory=list, max_items=20)
    CTAs: List[str] = Field(default_factory=list, max_items=10)
    trust_signals: List[str] = Field(default_factory=list, max_items=10)

class RebuildResponse(BaseModel):
    business_id: int
    rebuild: RebuildOutput

# ======================
# Demo Models
# ======================
class DemoRequest(BaseModel):
    business_id: int
    rebuild_json: RebuildOutput

class DemoOutput(BaseModel):
    demo_url: str = Field(..., max_length=500)
    preview_url: Optional[str] = Field(None, max_length=500)
    deployed: bool = True

class DemoResponse(BaseModel):
    business_id: int
    demo: DemoOutput

# ======================
# Pitch Models
# ======================
class PitchRequest(BaseModel):
    business_id: int
    rebuild_json: RebuildOutput
    demo_json: DemoOutput

class PitchOutput(BaseModel):
    executive_summary: str = Field(..., max_length=3000)
    revenue_opportunity: str = Field(..., max_length=500)
    before_after: str = Field(..., max_length=1000)
    outbound_email: str = Field(..., max_length=2000)
    followup_email: str = Field(..., max_length=1000)

class PitchResponse(BaseModel):
    business_id: int
    pitch: PitchOutput

# ======================
# Job & Status Models
# ======================
class JobStatus(BaseModel):
    job_id: int
    business_id: int
    stage: str
    status: str  # idle | processing | completed | failed | awaiting_approval
    data: Optional[Dict[str, Any]] = None
    last_error: Optional[str] = None
    updated_at: datetime

class StageDefinition(BaseModel):
    stage_name: str
    description: str
    order: int

# ======================
# Approval Models
# ======================
class ApprovalRequest(BaseModel):
    job_id: int
    approved: bool
    notes: Optional[str] = Field(None, max_length=500)

class ApprovalResponse(BaseModel):
    job_id: int
    status: str
    message: str
