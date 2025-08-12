"""
OGCR API Mockup Server

A FastAPI implementation of the OGCR API Specification for testing and development purposes.

License: MIT
Copyright (c) 2025 OGCR Consortium
"""

from fastapi import FastAPI, HTTPException, Depends, Query, Path
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid
import json
from enum import Enum

# Initialize FastAPI app
app = FastAPI(
    title="OGCR API",
    description="OGCR API Specification Implementation",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Enums
class ProjectStatus(str, Enum):
    draft = "draft"
    submitted = "submitted"
    under_review = "under_review"
    approved = "approved"
    rejected = "rejected"
    archived = "archived"

class ProjectType(str, Enum):
    afforestation = "afforestation"
    reforestation = "reforestation"
    soil_carbon = "soil_carbon"
    biochar = "biochar"
    direct_air_capture = "direct_air_capture"
    enhanced_weathering = "enhanced_weathering"
    blue_carbon = "blue_carbon"
    biomass_energy_ccs = "biomass_energy_ccs"

class VerificationStatus(str, Enum):
    unverified = "unverified"
    pending = "pending"
    verified = "verified"
    rejected = "rejected"

# Pydantic Models
class Geometry(BaseModel):
    type: str = Field(..., pattern="^(Point|LineString|Polygon|MultiPoint|MultiLineString|MultiPolygon)$")
    coordinates: List[Any]

class MethodologyReference(BaseModel):
    id: str = Field(..., min_length=1, max_length=100)
    version: str = Field(..., pattern=r"^\d+\.\d+(\.\d+)?$")
    name: Optional[str] = Field(None, max_length=200)
    type: Optional[str] = Field(None, max_length=100)

class LedgerReference(BaseModel):
    transaction_id: str = Field(..., min_length=1)
    block_number: int = Field(..., ge=0)
    timestamp: datetime
    ledger_id: str = Field(..., min_length=1)

class Link(BaseModel):
    rel: str = Field(..., pattern="^(self|related-mrv|methodology|monitor|predecessor|successor|supporting-doc|data-source)$")
    href: str = Field(..., pattern=r"^https?://")
    type: Optional[str] = None
    title: Optional[str] = Field(None, max_length=200)

class PDDProperties(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=2000)
    creation_date: datetime
    last_updated: Optional[datetime] = None
    project_type: ProjectType
    status: ProjectStatus
    actor_id: str = Field(..., min_length=1, max_length=100)
    methodology: Optional[MethodologyReference] = None
    baseline_scenario: Optional[str] = Field(None, max_length=1000)
    expected_annual_benefit: Optional[float] = Field(None, ge=0)

class ProjectDesignDocument(BaseModel):
    type: str = Field("Feature", pattern="^Feature$")
    id: Optional[str] = Field(None, pattern="^[a-zA-Z0-9_-]+$", min_length=1, max_length=100)
    ogcr_version: str = Field(..., pattern=r"^\d+\.\d+\.\d+$")
    profile: str = Field("pdd", pattern="^pdd$")
    geometry: Geometry
    bbox: Optional[List[float]] = Field(None, min_length=4, max_length=4)
    properties: PDDProperties
    ledger_reference: Optional[LedgerReference] = None
    links: Optional[List[Link]] = None

class NetRemovalEstimate(BaseModel):
    value: float = Field(..., ge=0)
    unit: str = Field(..., pattern="^(tCO2e|kgCO2e|tCO2|kgCO2)$")
    basis: Optional[str] = Field(None, max_length=500)

class Uncertainty(BaseModel):
    min: float
    max: float
    confidence_level: float = Field(..., ge=0, le=1)

class VerifierInfo(BaseModel):
    organization: str = Field(..., min_length=1, max_length=200)
    accreditation_id: Optional[str] = Field(None, max_length=100)
    reviewer_name: Optional[str] = Field(None, max_length=100)

class MethodologyData(BaseModel):
    parameters: Dict[str, Any]
    measurement_devices: Optional[List[Dict[str, Any]]] = None
    sampling_strategy: Optional[str] = Field(None, max_length=500)
    data_quality_flags: Optional[Dict[str, Any]] = None
    processing_notes: Optional[str] = Field(None, max_length=2000)

class MRVProperties(BaseModel):
    project_id: str = Field(..., min_length=1, max_length=100)
    methodology_id: str = Field(..., min_length=1, max_length=100)
    start_date: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$")
    end_date: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$")
    methodology_data: MethodologyData
    net_removal_estimate: NetRemovalEstimate
    total_uncertainty: Optional[Uncertainty] = None
    verification_status: VerificationStatus = VerificationStatus.unverified
    verification_date: Optional[datetime] = None
    verifier_info: Optional[VerifierInfo] = None

class MRVDocument(BaseModel):
    type: str = Field("Feature", pattern="^Feature$")
    id: Optional[str] = Field(None, pattern="^[a-zA-Z0-9_-]+$", min_length=1, max_length=100)
    ogcr_version: str = Field(..., pattern=r"^\d+\.\d+\.\d+$")
    profile: str = Field("mrv", pattern="^mrv$")
    geometry: Geometry
    bbox: Optional[List[float]] = Field(None, min_length=4, max_length=4)
    properties: MRVProperties
    ledger_reference: Optional[LedgerReference] = None
    links: Optional[List[Link]] = None

class CarbonCredit(BaseModel):
    token_id: str
    project_id: str
    mrv_id: str
    vintage_year: int
    carbon_amount: float
    status: str
    owner: str
    serial_number: str
    issuance_date: datetime
    retired: bool = False
    retirement_timestamp: Optional[datetime] = None

class PaginationResponse(BaseModel):
    total: int
    limit: int
    offset: int
    has_more: bool

class ProjectListResponse(BaseModel):
    data: List[Dict[str, Any]]
    pagination: PaginationResponse

# In-memory storage (for mockup purposes)
projects_db = {}
mrv_db = {}
credits_db = {}

# Authentication dependency
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    # Mock authentication - in real implementation, validate JWT token
    if not credentials.credentials:
        raise HTTPException(status_code=401, detail="Authentication required")
    return {"user_id": "mock_user", "roles": ["developer"]}

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "0.1.0"
    }

# Project endpoints
@app.post("/projects", status_code=201)
async def create_project(
    project: ProjectDesignDocument,
    current_user: dict = Depends(get_current_user)
):
    """Create a new carbon removal project"""
    project_id = str(uuid.uuid4())
    project.id = project_id
    project.properties.creation_date = datetime.utcnow()
    project.properties.last_updated = datetime.utcnow()
    
    # Store in mock database
    projects_db[project_id] = project.model_dump()
    
    return {
        "id": project_id,
        "status": project.properties.status,
        "created_at": project.properties.creation_date.isoformat(),
        "validation_results": {
            "schema_valid": True,
            "geometry_valid": True,
            "methodology_valid": True
        }
    }

@app.get("/projects/{project_id}")
async def get_project(
    project_id: str = Path(..., pattern="^[a-zA-Z0-9_-]+$")
):
    """Get project details"""
    if project_id not in projects_db:
        raise HTTPException(status_code=404, detail="Project not found")
    
    return projects_db[project_id]

@app.get("/projects", response_model=ProjectListResponse)
async def list_projects(
    status: Optional[ProjectStatus] = Query(None),
    project_type: Optional[ProjectType] = Query(None),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    """List projects with filtering and pagination"""
    filtered_projects = []
    
    for project_data in projects_db.values():
        if status and project_data["properties"]["status"] != status.value:
            continue
        if project_type and project_data["properties"]["project_type"] != project_type.value:
            continue
        filtered_projects.append({
            "id": project_data["id"],
            "name": project_data["properties"]["name"],
            "status": project_data["properties"]["status"],
            "project_type": project_data["properties"]["project_type"],
            "created_at": project_data["properties"]["creation_date"]
        })
    
    total = len(filtered_projects)
    paginated_projects = filtered_projects[offset:offset + limit]
    
    return ProjectListResponse(
        data=paginated_projects,
        pagination=PaginationResponse(
            total=total,
            limit=limit,
            offset=offset,
            has_more=offset + limit < total
        )
    )

@app.put("/projects/{project_id}")
async def update_project(
    project_id: str,
    project: ProjectDesignDocument,
    current_user: dict = Depends(get_current_user)
):
    """Update an existing project (only allowed for draft status)"""
    if project_id not in projects_db:
        raise HTTPException(status_code=404, detail="Project not found")
    
    existing_project = projects_db[project_id]
    if existing_project["properties"]["status"] != "draft":
        raise HTTPException(status_code=400, detail="Only draft projects can be updated")
    
    project.id = project_id
    project.properties.last_updated = datetime.utcnow()
    projects_db[project_id] = project.model_dump()
    
    return projects_db[project_id]

@app.post("/projects/{project_id}/submit")
async def submit_project(
    project_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Submit project for approval"""
    if project_id not in projects_db:
        raise HTTPException(status_code=404, detail="Project not found")
    
    project = projects_db[project_id]
    if project["properties"]["status"] != "draft":
        raise HTTPException(status_code=400, detail="Only draft projects can be submitted")
    
    # Update status
    project["properties"]["status"] = "submitted"
    project["properties"]["last_updated"] = datetime.utcnow().isoformat()
    
    # Mock blockchain reference
    project["ledger_reference"] = {
        "transaction_id": f"0x{uuid.uuid4().hex}",
        "block_number": 18765432,
        "timestamp": datetime.utcnow().isoformat(),
        "ledger_id": "ethereum-mainnet"
    }
    
    return {
        "status": "submitted",
        "blockchain_reference": project["ledger_reference"],
        "submitted_at": project["properties"]["last_updated"]
    }

@app.post("/projects/{project_id}/approve")
async def approve_project(
    project_id: str,
    approval_data: dict,
    current_user: dict = Depends(get_current_user)
):
    """Approve a submitted project (validator only)"""
    if project_id not in projects_db:
        raise HTTPException(status_code=404, detail="Project not found")
    
    project = projects_db[project_id]
    if project["properties"]["status"] != "submitted":
        raise HTTPException(status_code=400, detail="Only submitted projects can be approved")
    
    # Update status
    project["properties"]["status"] = "approved"
    project["properties"]["last_updated"] = datetime.utcnow().isoformat()
    
    return {
        "status": "approved",
        "approved_at": project["properties"]["last_updated"],
        "approved_by": current_user["user_id"]
    }

# MRV endpoints
@app.post("/projects/{project_id}/monitoring", status_code=201)
async def create_mrv_report(
    project_id: str,
    mrv: MRVDocument,
    current_user: dict = Depends(get_current_user)
):
    """Submit MRV report for a project"""
    if project_id not in projects_db:
        raise HTTPException(status_code=404, detail="Project not found")
    
    project = projects_db[project_id]
    if project["properties"]["status"] != "approved":
        raise HTTPException(status_code=400, detail="Only approved projects can accept MRV reports")
    
    mrv_id = str(uuid.uuid4())
    mrv.id = mrv_id
    mrv.properties.project_id = project_id
    
    # Store in mock database
    mrv_db[mrv_id] = mrv.model_dump()
    
    return {
        "id": mrv_id,
        "status": "pending_verification",
        "created_at": datetime.utcnow().isoformat(),
        "validation_results": {
            "temporal_valid": True,
            "methodology_compliant": True,
            "no_overlaps": True
        }
    }

@app.get("/projects/{project_id}/monitoring/{mrv_id}")
async def get_mrv_report(project_id: str, mrv_id: str):
    """Get MRV report details"""
    if mrv_id not in mrv_db:
        raise HTTPException(status_code=404, detail="MRV report not found")
    
    mrv_report = mrv_db[mrv_id]
    if mrv_report["properties"]["project_id"] != project_id:
        raise HTTPException(status_code=404, detail="MRV report not found for this project")
    
    return mrv_report

@app.get("/projects/{project_id}/monitoring")
async def list_mrv_reports(
    project_id: str,
    status: Optional[VerificationStatus] = Query(None),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    """List MRV reports for a project"""
    if project_id not in projects_db:
        raise HTTPException(status_code=404, detail="Project not found")
    
    filtered_reports = []
    for mrv_data in mrv_db.values():
        if mrv_data["properties"]["project_id"] != project_id:
            continue
        if status and mrv_data["properties"]["verification_status"] != status.value:
            continue
        filtered_reports.append(mrv_data)
    
    total = len(filtered_reports)
    paginated_reports = filtered_reports[offset:offset + limit]
    
    return {
        "data": paginated_reports,
        "pagination": {
            "total": total,
            "limit": limit,
            "offset": offset,
            "has_more": offset + limit < total
        }
    }

@app.post("/projects/{project_id}/monitoring/{mrv_id}/verify")
async def verify_mrv_report(
    project_id: str,
    mrv_id: str,
    verification_data: dict,
    current_user: dict = Depends(get_current_user)
):
    """Verify MRV report (verifier only)"""
    if mrv_id not in mrv_db:
        raise HTTPException(status_code=404, detail="MRV report not found")
    
    mrv_report = mrv_db[mrv_id]
    if mrv_report["properties"]["project_id"] != project_id:
        raise HTTPException(status_code=404, detail="MRV report not found for this project")
    
    # Update verification status
    mrv_report["properties"]["verification_status"] = "verified"
    mrv_report["properties"]["verification_date"] = datetime.utcnow().isoformat()
    
    return {
        "status": "verified",
        "verified_at": mrv_report["properties"]["verification_date"],
        "verified_by": current_user["user_id"],
        "verified_removals": verification_data.get("verified_removals", 0)
    }

# Credit endpoints
@app.get("/credits")
async def list_credits(
    status: Optional[str] = Query(None),
    project_id: Optional[str] = Query(None),
    vintage: Optional[int] = Query(None),
    owner: Optional[str] = Query(None),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    """List carbon credits with filtering"""
    filtered_credits = []
    
    for credit_data in credits_db.values():
        if status and credit_data["status"] != status:
            continue
        if project_id and credit_data["project_id"] != project_id:
            continue
        if vintage and credit_data["vintage_year"] != vintage:
            continue
        if owner and credit_data["owner"] != owner:
            continue
        filtered_credits.append(credit_data)
    
    total = len(filtered_credits)
    paginated_credits = filtered_credits[offset:offset + limit]
    
    return {
        "data": paginated_credits,
        "pagination": {
            "total": total,
            "limit": limit,
            "offset": offset,
            "has_more": offset + limit < total
        }
    }

@app.get("/credits/{credit_id}")
async def get_credit_details(credit_id: str):
    """Get credit details"""
    if credit_id not in credits_db:
        raise HTTPException(status_code=404, detail="Credit not found")
    
    return credits_db[credit_id]

@app.post("/credits/transfer")
async def transfer_credits(
    transfer_data: dict,
    current_user: dict = Depends(get_current_user)
):
    """Transfer credits to another owner"""
    credit_ids = transfer_data.get("credit_ids", [])
    recipient = transfer_data.get("recipient")
    
    if not credit_ids or not recipient:
        raise HTTPException(status_code=400, detail="Missing credit_ids or recipient")
    
    # Mock transfer logic
    transfer_id = str(uuid.uuid4())
    
    return {
        "transfer_id": transfer_id,
        "status": "pending",
        "blockchain_transaction": f"0x{uuid.uuid4().hex}"
    }

@app.post("/credits/{credit_id}/retire")
async def retire_credit(
    credit_id: str,
    retirement_data: dict,
    current_user: dict = Depends(get_current_user)
):
    """Retire a carbon credit"""
    if credit_id not in credits_db:
        raise HTTPException(status_code=404, detail="Credit not found")
    
    credit = credits_db[credit_id]
    if credit["retired"]:
        raise HTTPException(status_code=400, detail="Credit already retired")
    
    # Update retirement status
    credit["retired"] = True
    credit["retirement_timestamp"] = datetime.utcnow().isoformat()
    
    return {
        "status": "retired",
        "retired_at": credit["retirement_timestamp"],
        "retirement_certificate": f"cert_{uuid.uuid4().hex[:12]}"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

