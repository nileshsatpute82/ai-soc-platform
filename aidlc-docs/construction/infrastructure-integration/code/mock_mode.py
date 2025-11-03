"""Mock mode for immediate deployment without AWS dependencies."""

import json
import time
from typing import Dict, Any, List
from datetime import datetime

class MockBedrockClient:
    """Mock Bedrock client for demo purposes."""
    
    def __init__(self, config_service=None):
        self.config = config_service
    
    def invoke_claude(self, prompt: str, model_id: str = None) -> Dict[str, Any]:
        """Mock Claude invocation."""
        return {
            "content": [{"text": f"Mock AI response to: {prompt[:50]}..."}],
            "usage": {"input_tokens": 100, "output_tokens": 50}
        }
    
    def health_check(self) -> Dict[str, Any]:
        return {"status": "healthy", "mode": "mock"}

class MockRDSClient:
    """Mock RDS client for demo purposes."""
    
    def __init__(self, config_service=None):
        self.config = config_service
        self.mock_data = []
    
    def execute_query(self, query: str, params: tuple = None) -> list:
        return [("mock_result", "demo_data")]
    
    def execute_command(self, command: str, params: tuple = None) -> int:
        return 1
    
    def health_check(self) -> Dict[str, Any]:
        return {"status": "healthy", "mode": "mock"}

class MockDocumentDBClient:
    """Mock DocumentDB client for demo purposes."""
    
    def __init__(self, config_service=None):
        self.config = config_service
        self.mock_collections = {}
    
    def insert_document(self, collection_name: str, document: Dict[str, Any]) -> str:
        return "mock_id_123"
    
    def find_documents(self, collection_name: str, query: Dict[str, Any] = None, limit: int = None) -> list:
        return [{"_id": "mock_id", "data": "mock_document"}]
    
    def health_check(self) -> Dict[str, Any]:
        return {"status": "healthy", "mode": "mock"}

class MockElastiCacheClient:
    """Mock ElastiCache client for demo purposes."""
    
    def __init__(self, config_service=None):
        self.config = config_service
        self.cache = {}
    
    def set(self, key: str, value: Any, ttl: int = None) -> bool:
        self.cache[key] = value
        return True
    
    def get(self, key: str, as_json: bool = False) -> Any:
        return self.cache.get(key, "mock_cached_value")
    
    def health_check(self) -> Dict[str, Any]:
        return {"status": "healthy", "mode": "mock"}

class MockSQSClient:
    """Mock SQS client for demo purposes."""
    
    def __init__(self, config_service=None):
        self.config = config_service
        self.queues = {}
    
    def send_message(self, queue_name: str, message: Dict[str, Any], delay_seconds: int = 0) -> str:
        return "mock_message_id"
    
    def receive_messages(self, queue_name: str, max_messages: int = 1, wait_time: int = 20) -> List[Dict[str, Any]]:
        return [{"message_id": "mock_id", "body": {"mock": "message"}}]
    
    def health_check(self) -> Dict[str, Any]:
        return {"status": "healthy", "mode": "mock"}

class MockConfigurationService:
    """Mock configuration service."""
    
    def __init__(self):
        self.config = {
            "MOCK_MODE": "true",
            "AWS_REGION": "us-east-1",
            "FLASK_ENV": "production"
        }
    
    def get(self, key: str, default: str = None) -> str:
        return self.config.get(key, default)
    
    def set(self, key: str, value: str):
        self.config[key] = value
    
    def get_all_config(self) -> Dict[str, str]:
        return self.config.copy()
    
    def health_check(self) -> Dict[str, Any]:
        return {"status": "healthy", "mode": "mock"}

class MockAuditService:
    """Mock audit service."""
    
    def __init__(self, config_service=None):
        self.config = config_service
        self.events = []
    
    def log_event(self, event_type: str, severity: str, details: Dict[str, Any] = None, user_id: str = None, session_id: str = None) -> str:
        event_id = f"mock_event_{len(self.events)}"
        self.events.append({
            "id": event_id,
            "event_type": event_type,
            "severity": severity,
            "details": details or {},
            "timestamp": datetime.utcnow().isoformat()
        })
        return event_id
    
    def get_events(self, filters: Dict = None, limit: int = 100, offset: int = 0) -> List[Dict]:
        return self.events[offset:offset+limit]
    
    def health_check(self) -> Dict[str, Any]:
        return {"status": "healthy", "mode": "mock"}

class MockMITREComponent:
    """Mock MITRE component."""
    
    def __init__(self, data_storage=None, config_service=None):
        self.config = config_service
        self.mock_techniques = [
            {"id": "T1566", "name": "Phishing", "tactic": "Initial Access"},
            {"id": "T1059", "name": "Command and Scripting Interpreter", "tactic": "Execution"}
        ]
    
    def get_techniques(self, tactic: str = None, platform: str = None) -> List[Dict]:
        return self.mock_techniques
    
    def get_technique_by_id(self, technique_id: str) -> Dict:
        return {"id": technique_id, "name": "Mock Technique", "description": "Demo technique"}
    
    def map_to_mitre(self, indicators: List[str]) -> Dict[str, Any]:
        return {
            "techniques": self.mock_techniques,
            "confidence": 0.85,
            "mapped_indicators": len(indicators)
        }
    
    def health_check(self) -> Dict[str, Any]:
        return {"status": "healthy", "mode": "mock"}