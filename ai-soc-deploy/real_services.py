"""Real audit and MITRE services using database."""

import time
import json
from typing import Dict, Any, List
from datetime import datetime

class RealAuditService:
    """Real audit service using PostgreSQL database."""
    
    def __init__(self, rds_client, config_service):
        self.rds = rds_client
        self.config = config_service
    
    def log_event(self, event_type: str, severity: str, details: Dict[str, Any], user_name: str = None, source: str = None) -> str:
        """Log audit event to database."""
        try:
            event_id = f"audit_{int(time.time())}_{hash(str(details)) % 10000}"
            
            self.rds.execute_command("""
                INSERT INTO audit_events (event_id, event_type, severity, user_name, source, details)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (event_id, event_type, severity, user_name, source, json.dumps(details)))
            
            return event_id
        except Exception as e:
            print(f"Error logging audit event: {e}")
            return f"error_{int(time.time())}"
    
    def get_events(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get audit events from database."""
        try:
            result = self.rds.execute_query("""
                SELECT event_id, event_type, severity, user_name, source, details, timestamp
                FROM audit_events
                ORDER BY timestamp DESC
                LIMIT %s
            """, (limit,))
            
            events = []
            for row in result:
                try:
                    details = json.loads(row[5]) if row[5] else {}
                except:
                    details = {}
                
                events.append({
                    'event_id': row[0],
                    'event_type': row[1],
                    'severity': row[2],
                    'user_name': row[3],
                    'source': row[4],
                    'details': details,
                    'timestamp': row[6].isoformat() if hasattr(row[6], 'isoformat') else str(row[6])
                })
            
            return events
        except Exception as e:
            print(f"Error getting audit events: {e}")
            return []
    
    def health_check(self) -> Dict[str, Any]:
        """Check audit service health."""
        try:
            # Test database connection
            result = self.rds.execute_query("SELECT COUNT(*) FROM audit_events")
            event_count = result[0][0] if result else 0
            
            return {
                'status': 'healthy',
                'mode': 'real_database',
                'total_events': event_count,
                'service': 'audit'
            }
        except Exception as e:
            return {
                'status': 'unhealthy',
                'mode': 'real_database',
                'error': str(e),
                'service': 'audit'
            }

class RealMITREComponent:
    """Real MITRE ATT&CK component using PostgreSQL database."""
    
    def __init__(self, rds_client, config_service):
        self.rds = rds_client
        self.config = config_service
    
    def get_techniques(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Get MITRE techniques from database."""
        try:
            result = self.rds.execute_query("""
                SELECT technique_id, technique_name, tactic, description, detection_count, last_detected
                FROM mitre_techniques
                ORDER BY detection_count DESC, technique_id
                LIMIT %s
            """, (limit,))
            
            techniques = []
            for row in result:
                techniques.append({
                    'technique_id': row[0],
                    'technique_name': row[1],
                    'tactic': row[2],
                    'description': row[3],
                    'detection_count': row[4] or 0,
                    'detected_at': row[5].isoformat() if row[5] and hasattr(row[5], 'isoformat') else None,
                    'severity': 'MEDIUM'  # Default severity
                })
            
            return techniques
        except Exception as e:
            print(f"Error getting MITRE techniques: {e}")
            return []
    
    def map_to_mitre(self, indicators: List[str]) -> List[str]:
        """Map security indicators to MITRE techniques."""
        try:
            # Simple mapping logic
            mitre_mapping = {
                'suspicious_login': ['T1078'],
                'failed_auth': ['T1110'],
                'user_creation': ['T1136'],
                'privilege_escalation': ['T1098'],
                'account_discovery': ['T1087'],
                'CreateUser': ['T1136'],
                'DeleteUser': ['T1098'],
                'AttachUserPolicy': ['T1098'],
                'DetachUserPolicy': ['T1098']
            }
            
            mapped_techniques = []
            for indicator in indicators:
                for key, techniques in mitre_mapping.items():
                    if key.lower() in indicator.lower():
                        mapped_techniques.extend(techniques)
            
            # Remove duplicates and format
            unique_techniques = list(set(mapped_techniques))
            formatted_techniques = []
            
            for tech_id in unique_techniques:
                # Get technique details from database
                result = self.rds.execute_query("""
                    SELECT technique_name FROM mitre_techniques WHERE technique_id = %s
                """, (tech_id,))
                
                if result:
                    tech_name = result[0][0]
                    formatted_techniques.append(f"{tech_id} - {tech_name}")
                else:
                    formatted_techniques.append(tech_id)
            
            return formatted_techniques
        except Exception as e:
            print(f"Error mapping to MITRE: {e}")
            return []
    
    def get_technique_stats(self) -> Dict[str, Any]:
        """Get MITRE technique statistics."""
        try:
            # Total techniques
            total_result = self.rds.execute_query("SELECT COUNT(*) FROM mitre_techniques")
            total_techniques = total_result[0][0] if total_result else 0
            
            # Active techniques (detected in last 30 days)
            active_result = self.rds.execute_query("""
                SELECT COUNT(*) FROM mitre_techniques 
                WHERE last_detected > NOW() - INTERVAL '30 days'
            """)
            active_techniques = active_result[0][0] if active_result else 0
            
            # Top tactic
            tactic_result = self.rds.execute_query("""
                SELECT tactic, SUM(detection_count) as total_detections
                FROM mitre_techniques
                GROUP BY tactic
                ORDER BY total_detections DESC
                LIMIT 1
            """)
            top_tactic = tactic_result[0][0] if tactic_result else 'Initial Access'
            
            # Total detections
            detections_result = self.rds.execute_query("""
                SELECT SUM(detection_count) FROM mitre_techniques
            """)
            total_detections = detections_result[0][0] if detections_result and detections_result[0][0] else 0
            
            return {
                'total_techniques': total_techniques,
                'active_techniques': active_techniques,
                'top_tactic': top_tactic,
                'total_detections': total_detections
            }
        except Exception as e:
            print(f"Error getting MITRE stats: {e}")
            return {
                'total_techniques': 0,
                'active_techniques': 0,
                'top_tactic': 'Unknown',
                'total_detections': 0
            }
    
    def health_check(self) -> Dict[str, Any]:
        """Check MITRE component health."""
        try:
            stats = self.get_technique_stats()
            return {
                'status': 'healthy',
                'mode': 'real_database',
                'techniques_loaded': stats['total_techniques'],
                'service': 'mitre'
            }
        except Exception as e:
            return {
                'status': 'unhealthy',
                'mode': 'real_database',
                'error': str(e),
                'service': 'mitre'
            }