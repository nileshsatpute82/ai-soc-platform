import json
import boto3
from datetime import datetime, timedelta
from typing import Dict, Any, List
from enum import Enum

class AuditTier(Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"

class AuditService:
    def __init__(self):
        self.cloudwatch = boto3.client('logs')
        self.log_groups = {
            AuditTier.CRITICAL: '/ai-soc/audit/critical',
            AuditTier.HIGH: '/ai-soc/audit/high',
            AuditTier.MEDIUM: '/ai-soc/audit/medium',
            AuditTier.LOW: '/ai-soc/audit/low'
        }
        self.retention_policies = {
            AuditTier.CRITICAL: 2555,  # 7 years in days
            AuditTier.HIGH: 1095,      # 3 years
            AuditTier.MEDIUM: 365,     # 1 year
            AuditTier.LOW: 90          # 90 days
        }
    
    def log_event(self, event_type: str, user_id: str = None, component: str = None, 
                  action: str = None, resource: str = None, result: str = "SUCCESS", 
                  details: Dict[str, Any] = None) -> str:
        """Log audit event with automatic tier classification"""
        
        # Classify event tier
        tier = self._classify_event_tier(event_type, action, result)
        
        # Create audit event
        audit_event = {
            "event_id": self._generate_event_id(),
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": event_type,
            "tier": tier.value,
            "user_id": user_id,
            "component": component,
            "action": action,
            "resource": resource,
            "result": result,
            "details": details or {},
            "retention_expiry": self._calculate_retention_expiry(tier)
        }
        
        # Log to appropriate tier
        self._write_to_cloudwatch(tier, audit_event)
        
        return audit_event["event_id"]
    
    def _classify_event_tier(self, event_type: str, action: str, result: str) -> AuditTier:
        """Classify event into appropriate audit tier"""
        
        # Security events are always critical
        if event_type in ["SECURITY_EVENT", "AUTHENTICATION_FAILURE", "AUTHORIZATION_FAILURE"]:
            return AuditTier.CRITICAL
        
        # Failed actions are high priority
        if result == "FAILURE":
            return AuditTier.HIGH
        
        # User actions are high priority
        if event_type == "USER_ACTION":
            return AuditTier.HIGH
        
        # System operations are medium priority
        if event_type == "SYSTEM_OPERATION":
            return AuditTier.MEDIUM
        
        # Everything else is low priority
        return AuditTier.LOW
    
    def _generate_event_id(self) -> str:
        """Generate unique event ID"""
        import uuid
        return str(uuid.uuid4())
    
    def _calculate_retention_expiry(self, tier: AuditTier) -> str:
        """Calculate retention expiry date"""
        retention_days = self.retention_policies[tier]
        expiry_date = datetime.utcnow() + timedelta(days=retention_days)
        return expiry_date.isoformat()
    
    def _write_to_cloudwatch(self, tier: AuditTier, event: Dict[str, Any]):
        """Write audit event to CloudWatch Logs"""
        try:
            log_group = self.log_groups[tier]
            log_stream = f"audit-{datetime.utcnow().strftime('%Y-%m-%d')}"
            
            # Create log stream if it doesn't exist
            try:
                self.cloudwatch.create_log_stream(
                    logGroupName=log_group,
                    logStreamName=log_stream
                )
            except self.cloudwatch.exceptions.ResourceAlreadyExistsException:
                pass
            
            # Put log event
            self.cloudwatch.put_log_events(
                logGroupName=log_group,
                logStreamName=log_stream,
                logEvents=[{
                    'timestamp': int(datetime.utcnow().timestamp() * 1000),
                    'message': json.dumps(event)
                }]
            )
        except Exception as e:
            # Fallback to local logging if CloudWatch fails
            print(f"CloudWatch logging failed: {e}")
            print(f"Audit Event: {json.dumps(event)}")
    
    def query_audit_events(self, start_time: datetime, end_time: datetime, 
                          tier: AuditTier = None, event_type: str = None) -> List[Dict[str, Any]]:
        """Query audit events with filters"""
        try:
            log_groups_to_query = [self.log_groups[tier]] if tier else list(self.log_groups.values())
            
            events = []
            for log_group in log_groups_to_query:
                response = self.cloudwatch.filter_log_events(
                    logGroupName=log_group,
                    startTime=int(start_time.timestamp() * 1000),
                    endTime=int(end_time.timestamp() * 1000)
                )
                
                for event in response.get('events', []):
                    try:
                        parsed_event = json.loads(event['message'])
                        if not event_type or parsed_event.get('event_type') == event_type:
                            events.append(parsed_event)
                    except json.JSONDecodeError:
                        continue
            
            return events
        except Exception as e:
            print(f"Error querying audit events: {e}")
            return []