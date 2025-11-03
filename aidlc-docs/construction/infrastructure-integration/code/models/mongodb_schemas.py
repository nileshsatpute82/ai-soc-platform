from datetime import datetime
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field

class FlexibleDataDocument(BaseModel):
    """Schema for flexible investigation data in MongoDB"""
    data: Dict[str, Any]
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class InvestigationFinding(BaseModel):
    """Schema for investigation findings"""
    investigation_id: str
    finding_type: str
    content: Dict[str, Any]
    confidence_score: float = Field(ge=0.0, le=1.0)
    source_component: str
    mitre_mappings: List[Dict[str, Any]] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)

class AIAnalysisResult(BaseModel):
    """Schema for AI analysis results"""
    analysis_id: str
    request_id: str
    model_used: str
    prompt: str
    response: Dict[str, Any]
    processing_time: float
    token_usage: Dict[str, int] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)

class MITREMapping(BaseModel):
    """Schema for MITRE ATT&CK mappings"""
    technique_id: str
    technique_name: str
    tactics: List[str]
    confidence: float = Field(ge=0.0, le=1.0)
    evidence: List[str] = Field(default_factory=list)
    mapped_at: datetime = Field(default_factory=datetime.utcnow)

class ThreatIntelligence(BaseModel):
    """Schema for threat intelligence data"""
    indicator: str
    indicator_type: str  # ip, domain, hash, etc.
    threat_type: str
    severity: str
    source: str
    description: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    first_seen: datetime = Field(default_factory=datetime.utcnow)
    last_seen: datetime = Field(default_factory=datetime.utcnow)