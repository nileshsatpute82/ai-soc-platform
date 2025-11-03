"""Real AWS alert processor for security events."""

import boto3
import json
import time
from typing import Dict, Any, List
from datetime import datetime
from alert_storage import AlertStorage

class RealAlertProcessor:
    """Process real security alerts from AWS SQS."""
    
    def __init__(self, config_service, rds_client=None, documentdb_client=None):
        self.config = config_service
        self.sqs = boto3.client('sqs', region_name=self.config.get('AWS_REGION', 'us-east-1'))
        self.queue_url = self.config.get('AWS_SQS_QUEUE_URL')
        
        # Initialize alert storage if database clients provided
        self.storage = None
        if rds_client and documentdb_client:
            self.storage = AlertStorage(rds_client, documentdb_client)
    
    def poll_alerts(self, max_messages: int = 10) -> List[Dict[str, Any]]:
        """Poll SQS for new security alerts."""
        if not self.queue_url:
            return []
        
        try:
            response = self.sqs.receive_message(
                QueueUrl=self.queue_url,
                MaxNumberOfMessages=max_messages,
                WaitTimeSeconds=1,
                MessageAttributeNames=['All']
            )
            
            messages = response.get('Messages', [])
            alerts = []
            
            for message in messages:
                try:
                    # Parse message body
                    body = json.loads(message['Body'])
                    
                    # Handle SNS wrapped messages
                    if 'Message' in body:
                        alert_data = json.loads(body['Message'])
                    else:
                        alert_data = body
                    
                    # Convert to standard alert format
                    alert = self.convert_to_standard_alert(alert_data, message)
                    alerts.append(alert)
                    
                    # Save alert to persistent storage
                    if self.storage:
                        alert_id = self.storage.save_alert(alert)
                        if alert_id:
                            alert['stored_id'] = alert_id
                    
                    # Delete processed message
                    self.sqs.delete_message(
                        QueueUrl=self.queue_url,
                        ReceiptHandle=message['ReceiptHandle']
                    )
                    
                except Exception as e:
                    print(f"Error processing message: {e}")
                    continue
            
            return alerts
            
        except Exception as e:
            print(f"Error polling SQS: {e}")
            return []
    
    def convert_to_standard_alert(self, aws_event: Dict[str, Any], sqs_message: Dict[str, Any]) -> Dict[str, Any]:
        """Convert AWS CloudTrail event to standard alert format."""
        
        # Extract event details
        detail = aws_event.get('detail', {})
        event_name = detail.get('eventName', 'Unknown')
        event_source = detail.get('eventSource', aws_event.get('source', 'aws'))
        user_identity = detail.get('userIdentity', {})
        source_ip = detail.get('sourceIPAddress', 'Unknown')
        
        # Determine severity based on event type
        severity = self.determine_severity(event_name, user_identity, detail)
        
        # Create standardized alert
        alert = {
            'alert_id': f"aws-{aws_event.get('id', int(time.time()))}",
            'timestamp': aws_event.get('time', datetime.now().isoformat()),
            'source': 'AWS CloudTrail',
            'severity': severity,
            'event_type': aws_event.get('detail-type', 'AWS Security Event'),
            'description': self.generate_description(event_name, user_identity, detail),
            'source_ip': source_ip,
            'user': user_identity.get('userName', user_identity.get('type', 'Unknown')),
            'account_id': aws_event.get('account', 'Unknown'),
            'region': aws_event.get('region', 'Unknown'),
            'raw_event': aws_event,
            'mitre_tactics': self.map_mitre_tactics(event_name, detail),
            'recommendations': self.generate_recommendations(event_name, detail)
        }
        
        return alert
    
    def determine_severity(self, event_name: str, user_identity: Dict[str, Any], detail: Dict[str, Any]) -> str:
        """Determine alert severity based on event characteristics."""
        
        # Critical events
        if user_identity.get('type') == 'Root':
            return 'CRITICAL'
        
        if 'SigninFailure' in detail.get('errorCode', ''):
            return 'HIGH'
        
        if event_name in ['DeleteUser', 'DeleteRole', 'DetachUserPolicy']:
            return 'HIGH'
        
        if event_name in ['CreateUser', 'CreateRole', 'AttachUserPolicy']:
            return 'MEDIUM'
        
        return 'LOW'
    
    def generate_description(self, event_name: str, user_identity: Dict[str, Any], detail: Dict[str, Any]) -> str:
        """Generate human-readable alert description."""
        
        user = user_identity.get('userName', user_identity.get('type', 'Unknown user'))
        source_ip = detail.get('sourceIPAddress', 'unknown IP')
        
        if 'SigninFailure' in detail.get('errorCode', ''):
            return f"Failed login attempt by {user} from {source_ip}"
        
        if user_identity.get('type') == 'Root':
            return f"Root account access detected from {source_ip}"
        
        if event_name == 'CreateUser':
            new_user = detail.get('requestParameters', {}).get('userName', 'unknown')
            return f"New IAM user '{new_user}' created by {user}"
        
        if event_name == 'DeleteUser':
            deleted_user = detail.get('requestParameters', {}).get('userName', 'unknown')
            return f"IAM user '{deleted_user}' deleted by {user}"
        
        return f"AWS API call '{event_name}' by {user} from {source_ip}"
    
    def map_mitre_tactics(self, event_name: str, detail: Dict[str, Any]) -> List[str]:
        """Map events to MITRE ATT&CK tactics."""
        
        tactics = []
        
        if 'SigninFailure' in detail.get('errorCode', ''):
            tactics.extend(['T1110 - Brute Force', 'T1078 - Valid Accounts'])
        
        if event_name in ['CreateUser', 'CreateRole']:
            tactics.extend(['T1136 - Create Account', 'T1098 - Account Manipulation'])
        
        if event_name in ['AttachUserPolicy', 'DetachUserPolicy']:
            tactics.extend(['T1098 - Account Manipulation'])
        
        return tactics
    
    def generate_recommendations(self, event_name: str, detail: Dict[str, Any]) -> List[str]:
        """Generate security recommendations."""
        
        recommendations = []
        
        if 'SigninFailure' in detail.get('errorCode', ''):
            recommendations.extend([
                'Monitor for repeated failed login attempts',
                'Consider implementing account lockout policies',
                'Review source IP for known threat indicators'
            ])
        
        if event_name in ['CreateUser', 'CreateRole']:
            recommendations.extend([
                'Verify the legitimacy of the new account creation',
                'Review permissions assigned to the new account',
                'Ensure proper approval process was followed'
            ])
        
        return recommendations
    
    def get_stored_alerts(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get alerts from persistent storage."""
        if self.storage:
            return self.storage.get_alerts(limit=limit)
        return []
    
    def get_alert_statistics(self) -> Dict[str, Any]:
        """Get alert statistics from storage."""
        if self.storage:
            return self.storage.get_alert_statistics()
        return {'total_alerts': 0, 'by_severity': {}, 'by_status': {}, 'recent_24h': 0}
    
    def health_check(self) -> Dict[str, Any]:
        """Check real alert processor health."""
        try:
            health_data = {
                'service': 'real_alert_processor',
                'queue_configured': bool(self.queue_url),
                'storage_enabled': bool(self.storage)
            }
            
            if not self.queue_url:
                health_data.update({
                    'status': 'degraded',
                    'message': 'AWS_SQS_QUEUE_URL not configured'
                })
                return health_data
            
            # Test SQS access
            self.sqs.get_queue_attributes(
                QueueUrl=self.queue_url,
                AttributeNames=['ApproximateNumberOfMessages']
            )
            health_data['sqs_access'] = 'healthy'
            
            # Test storage if available
            if self.storage:
                storage_health = self.storage.health_check()
                health_data['storage'] = storage_health
            
            health_data.update({
                'status': 'healthy',
                'queue_url': self.queue_url
            })
            
            return health_data
            
        except Exception as e:
            return {
                'status': 'unhealthy',
                'service': 'real_alert_processor',
                'error': str(e),
                'queue_configured': bool(self.queue_url),
                'storage_enabled': bool(self.storage)
            }