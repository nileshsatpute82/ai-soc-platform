import json
import requests
from typing import Dict, List, Any, Optional
from datetime import datetime

class MITREAttackMappingComponent:
    def __init__(self):
        self.framework_data = {}
        self.current_version = None
        self.load_framework_data()
    
    def load_framework_data(self):
        """Load MITRE ATT&CK framework data"""
        try:
            # In production, this would load from a local cache or database
            # For now, using a minimal framework structure
            self.framework_data = {
                "tactics": {
                    "TA0001": {"name": "Initial Access", "description": "Gain initial foothold"},
                    "TA0002": {"name": "Execution", "description": "Execute malicious code"},
                    "TA0003": {"name": "Persistence", "description": "Maintain access"},
                    "TA0004": {"name": "Privilege Escalation", "description": "Gain higher privileges"},
                    "TA0005": {"name": "Defense Evasion", "description": "Avoid detection"}
                },
                "techniques": {
                    "T1566": {"name": "Phishing", "tactics": ["TA0001"], "description": "Email-based attacks"},
                    "T1059": {"name": "Command and Scripting Interpreter", "tactics": ["TA0002"], "description": "Execute commands"},
                    "T1053": {"name": "Scheduled Task/Job", "tactics": ["TA0002", "TA0003"], "description": "Schedule tasks"},
                    "T1055": {"name": "Process Injection", "tactics": ["TA0004", "TA0005"], "description": "Inject into processes"}
                }
            }
            self.current_version = "12.1"
        except Exception as e:
            print(f"Error loading MITRE framework: {e}")
    
    def map_findings_to_mitre(self, findings: Dict[str, Any]) -> Dict[str, Any]:
        """Map security findings to MITRE ATT&CK framework"""
        mappings = []
        
        # Simple keyword-based mapping (in production, this would use ML/NLP)
        finding_text = str(findings).lower()
        
        for technique_id, technique in self.framework_data["techniques"].items():
            if self._matches_technique(finding_text, technique):
                mappings.append({
                    "technique_id": technique_id,
                    "technique_name": technique["name"],
                    "tactics": [self.framework_data["tactics"][tactic_id]["name"] 
                              for tactic_id in technique["tactics"]],
                    "confidence": self._calculate_confidence(finding_text, technique)
                })
        
        return {
            "mappings": mappings,
            "framework_version": self.current_version,
            "mapped_at": datetime.utcnow().isoformat()
        }
    
    def _matches_technique(self, finding_text: str, technique: Dict[str, Any]) -> bool:
        """Check if finding matches technique"""
        keywords = {
            "T1566": ["phishing", "email", "attachment", "malicious link"],
            "T1059": ["command", "script", "powershell", "cmd", "bash"],
            "T1053": ["scheduled", "task", "cron", "job"],
            "T1055": ["injection", "process", "dll", "memory"]
        }
        
        technique_keywords = keywords.get(technique.get("id", ""), [])
        return any(keyword in finding_text for keyword in technique_keywords)
    
    def _calculate_confidence(self, finding_text: str, technique: Dict[str, Any]) -> float:
        """Calculate confidence score for mapping"""
        # Simple confidence calculation based on keyword matches
        return 0.8  # Default confidence
    
    def get_technique_details(self, technique_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a technique"""
        return self.framework_data["techniques"].get(technique_id)
    
    def get_tactic_details(self, tactic_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a tactic"""
        return self.framework_data["tactics"].get(tactic_id)
    
    def update_framework(self, new_version_data: Dict[str, Any]) -> bool:
        """Update framework data with validation"""
        try:
            # Validate new version data
            if self._validate_framework_data(new_version_data):
                # Backup current version
                backup = {
                    "version": self.current_version,
                    "data": self.framework_data,
                    "backup_time": datetime.utcnow().isoformat()
                }
                
                # Update to new version
                self.framework_data = new_version_data["data"]
                self.current_version = new_version_data["version"]
                
                return True
            return False
        except Exception as e:
            print(f"Error updating framework: {e}")
            return False
    
    def _validate_framework_data(self, data: Dict[str, Any]) -> bool:
        """Validate framework data structure"""
        required_keys = ["data", "version"]
        return all(key in data for key in required_keys)