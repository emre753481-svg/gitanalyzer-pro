"""
Pydantic models for GitAnalyzer Pro
"""
from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum


class AnalysisStatus(str, Enum):
    """Analysis status enumeration"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class ExportFormat(str, Enum):
    """Export format enumeration"""
    PDF = "pdf"
    MARKDOWN = "markdown"
    JSON = "json"


class AnalyzerType(str, Enum):
    """Available analyzer types"""
    SCOPE = "scope"
    UML = "uml"
    BPMN = "bpmn"
    FLOW = "flow"
    BUSINESS = "business"
    REQUIREMENTS = "requirements"
    ARCHITECTURE = "architecture"
    REPORTS = "reports"


class AnalysisRequest(BaseModel):
    """Request model for starting analysis"""
    repository_url: HttpUrl = Field(..., description="GitHub repository URL")
    github_token: str = Field(..., description="GitHub access token")
    analyzers: Optional[List[AnalyzerType]] = Field(
        default=None,
        description="Specific analyzers to run. If None, runs all."
    )
    ai_provider: Optional[str] = Field(default="anthropic", description="AI provider (anthropic/openai)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "repository_url": "https://github.com/owner/repo",
                "github_token": "ghp_xxxxxxxxxxxxx",
                "analyzers": ["scope", "architecture"],
                "ai_provider": "anthropic"
            }
        }


class AnalysisResponse(BaseModel):
    """Response model for analysis creation"""
    analysis_id: str = Field(..., description="Unique analysis ID")
    status: AnalysisStatus = Field(..., description="Current analysis status")
    created_at: datetime = Field(..., description="Analysis creation timestamp")
    repository_url: str = Field(..., description="Repository URL")
    
    class Config:
        json_schema_extra = {
            "example": {
                "analysis_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
                "status": "pending",
                "created_at": "2024-01-28T10:30:00Z",
                "repository_url": "https://github.com/owner/repo"
            }
        }


class AnalysisStatusResponse(BaseModel):
    """Response model for analysis status check"""
    analysis_id: str
    status: AnalysisStatus
    progress_percentage: int = Field(..., ge=0, le=100)
    current_step: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None


class ScopeDocument(BaseModel):
    """Project scope document"""
    project_overview: str
    objectives: List[str]
    scope_in: List[str]
    scope_out: List[str]
    assumptions: List[str]
    constraints: List[str]
    deliverables: List[str]


class UMLDiagrams(BaseModel):
    """UML diagrams collection"""
    use_case_diagram: str  # PlantUML or Mermaid syntax
    class_diagram: str
    sequence_diagrams: List[Dict[str, str]]
    activity_diagrams: List[Dict[str, str]]


class BPMNDiagrams(BaseModel):
    """BPMN diagrams"""
    business_processes: List[Dict[str, Any]]
    process_flows: List[str]  # BPMN notation


class FlowDiagrams(BaseModel):
    """Flow diagrams"""
    user_journey_maps: List[Dict[str, Any]]
    data_flow_diagrams: List[str]
    system_flow: str


class BusinessAnalysis(BaseModel):
    """Business analysis documents"""
    swot_analysis: Dict[str, List[str]]  # Strengths, Weaknesses, Opportunities, Threats
    roi_analysis: Dict[str, Any]
    stakeholder_analysis: List[Dict[str, str]]
    market_analysis: Dict[str, Any]


class Requirements(BaseModel):
    """Requirements documentation"""
    functional_requirements: List[Dict[str, str]]
    non_functional_requirements: List[Dict[str, str]]
    user_stories: List[Dict[str, str]]
    acceptance_criteria: List[Dict[str, str]]


class Architecture(BaseModel):
    """Architecture documentation"""
    system_architecture: str
    component_diagram: str
    deployment_diagram: str
    erd_diagram: str  # Entity Relationship Diagram
    api_documentation: Dict[str, Any]
    technology_stack: Dict[str, List[str]]


class Reports(BaseModel):
    """Analysis reports"""
    code_quality_score: float = Field(..., ge=0, le=100)
    code_metrics: Dict[str, Any]
    technical_debt: Dict[str, Any]
    security_issues: List[Dict[str, str]]
    performance_analysis: Dict[str, Any]
    recommendations: List[str]


class AnalysisResults(BaseModel):
    """Complete analysis results"""
    analysis_id: str
    repository_url: str
    analyzed_at: datetime
    scope_document: Optional[ScopeDocument] = None
    uml_diagrams: Optional[UMLDiagrams] = None
    bpmn_diagrams: Optional[BPMNDiagrams] = None
    flow_diagrams: Optional[FlowDiagrams] = None
    business_analysis: Optional[BusinessAnalysis] = None
    requirements: Optional[Requirements] = None
    architecture: Optional[Architecture] = None
    reports: Optional[Reports] = None


class ExportRequest(BaseModel):
    """Export request model"""
    format: ExportFormat = Field(..., description="Export format")
    include_diagrams: bool = Field(default=True, description="Include diagram images")
    
    class Config:
        json_schema_extra = {
            "example": {
                "format": "pdf",
                "include_diagrams": True
            }
        }


class ExportResponse(BaseModel):
    """Export response model"""
    download_url: str
    file_size_bytes: int
    format: ExportFormat
    expires_at: datetime


class HealthCheck(BaseModel):
    """Health check response"""
    status: str
    version: str
    timestamp: datetime
    services: Dict[str, str]
