from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from datetime import datetime

Base = declarative_base()

class StructuredData(Base):
    __tablename__ = 'structured_data'
    
    id = Column(Integer, primary_key=True)
    data = Column(JSON, nullable=False)
    metadata = Column(JSON)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class AuditEvent(Base):
    __tablename__ = 'audit_events'
    
    id = Column(Integer, primary_key=True)
    event_id = Column(String(36), unique=True, nullable=False)
    event_type = Column(String(50), nullable=False)
    tier = Column(String(20), nullable=False)
    user_id = Column(String(100))
    component = Column(String(100))
    action = Column(String(100))
    resource = Column(String(200))
    result = Column(String(20), nullable=False)
    details = Column(JSON)
    timestamp = Column(DateTime, default=func.now())
    retention_expiry = Column(DateTime)

class ConfigurationItem(Base):
    __tablename__ = 'configuration_items'
    
    id = Column(Integer, primary_key=True)
    key = Column(String(200), nullable=False)
    value = Column(Text)
    environment = Column(String(50), nullable=False)
    component = Column(String(100))
    is_secret = Column(Boolean, default=False)
    version = Column(Integer, default=1)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class SystemHealthMetric(Base):
    __tablename__ = 'system_health_metrics'
    
    id = Column(Integer, primary_key=True)
    component = Column(String(100), nullable=False)
    metric_name = Column(String(100), nullable=False)
    value = Column(String(100), nullable=False)
    unit = Column(String(20))
    status = Column(String(20), nullable=False)
    timestamp = Column(DateTime, default=func.now())
    tags = Column(JSON)