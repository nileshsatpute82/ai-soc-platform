"""Alert storage system for persistent alert management."""

import json
import time
from datetime import datetime
from typing import Dict, Any, List, Optional

class AlertStorage:
    """Manages persistent storage of security alerts."""
    
    def __init__(self, rds_client, documentdb_client):
        self.rds = rds_client
        self.documentdb = documentdb_client
        self.init_storage()
    
    def init_storage(self):
        """Initialize alert storage tables and collections."""
        try:
            # Create alerts table in RDS
            self.rds.execute_command("""
                CREATE TABLE IF NOT EXISTS security_alerts (
                    id SERIAL PRIMARY KEY,
                    alert_id VARCHAR(255) UNIQUE NOT NULL,
                    timestamp TIMESTAMP NOT NULL,
                    source VARCHAR(255) NOT NULL,
                    severity VARCHAR(50) NOT NULL,
                    event_type VARCHAR(255) NOT NULL,
                    description TEXT NOT NULL,
                    source_ip VARCHAR(45),
                    user_name VARCHAR(255),
                    account_id VARCHAR(50),
                    region VARCHAR(50),
                    mitre_tactics TEXT,
                    recommendations TEXT,
                    status VARCHAR(50) DEFAULT 'OPEN',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create indexes for performance
            self.rds.execute_command("""
                CREATE INDEX IF NOT EXISTS idx_alerts_timestamp ON security_alerts(timestamp);
                CREATE INDEX IF NOT EXISTS idx_alerts_severity ON security_alerts(severity);
                CREATE INDEX IF NOT EXISTS idx_alerts_status ON security_alerts(status);
                CREATE INDEX IF NOT EXISTS idx_alerts_source ON security_alerts(source);
            """)
            
        except Exception as e:
            print(f"Storage initialization error: {e}")
    
    def save_alert(self, alert: Dict[str, Any]) -> str:
        """Save alert to persistent storage."""
        try:
            # Save structured data to RDS
            alert_id = alert.get('alert_id', f"alert_{int(time.time())}")
            
            self.rds.execute_command("""
                INSERT INTO security_alerts (
                    alert_id, timestamp, source, severity, event_type, description,
                    source_ip, user_name, account_id, region, mitre_tactics, recommendations
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (alert_id) DO UPDATE SET
                    updated_at = CURRENT_TIMESTAMP
            """, (
                alert_id,
                alert.get('timestamp', datetime.now().isoformat()),
                alert.get('source', 'Unknown'),
                alert.get('severity', 'MEDIUM'),
                alert.get('event_type', 'Security Event'),
                alert.get('description', 'Security alert'),
                alert.get('source_ip'),
                alert.get('user'),
                alert.get('account_id'),
                alert.get('region'),
                json.dumps(alert.get('mitre_tactics', [])),
                json.dumps(alert.get('recommendations', []))
            ))
            
            # Save full raw data to DocumentDB for investigation
            investigation_doc = {
                'alert_id': alert_id,
                'timestamp': alert.get('timestamp', datetime.now().isoformat()),
                'raw_event': alert.get('raw_event', {}),
                'processed_data': alert,
                'investigation_status': 'pending',
                'created_at': datetime.now().isoformat()
            }
            
            self.documentdb.insert_document('security_investigations', investigation_doc)
            
            return alert_id
            
        except Exception as e:
            print(f"Error saving alert: {e}")
            return None
    
    def get_alerts(self, limit: int = 50, status: str = None, severity: str = None) -> List[Dict[str, Any]]:
        """Retrieve alerts from storage."""
        try:
            query = "SELECT * FROM security_alerts"
            params = []
            conditions = []
            
            if status:
                conditions.append("status = %s")
                params.append(status)
            
            if severity:
                conditions.append("severity = %s")
                params.append(severity)
            
            if conditions:
                query += " WHERE " + " AND ".join(conditions)
            
            query += " ORDER BY timestamp DESC LIMIT %s"
            params.append(limit)
            
            results = self.rds.execute_query(query, tuple(params))
            
            alerts = []
            for row in results:
                alert = {
                    'id': row[0],
                    'alert_id': row[1],
                    'timestamp': row[2].isoformat() if hasattr(row[2], 'isoformat') else str(row[2]),
                    'source': row[3],
                    'severity': row[4],
                    'event_type': row[5],
                    'description': row[6],
                    'source_ip': row[7],
                    'user': row[8],
                    'account_id': row[9],
                    'region': row[10],
                    'mitre_tactics': json.loads(row[11]) if row[11] else [],
                    'recommendations': json.loads(row[12]) if row[12] else [],
                    'status': row[13],
                    'created_at': row[14].isoformat() if hasattr(row[14], 'isoformat') else str(row[14]),
                    'updated_at': row[15].isoformat() if hasattr(row[15], 'isoformat') else str(row[15])
                }
                alerts.append(alert)
            
            return alerts
            
        except Exception as e:
            print(f"Error retrieving alerts: {e}")
            return []
    
    def update_alert_status(self, alert_id: str, status: str) -> bool:
        """Update alert status."""
        try:
            result = self.rds.execute_command("""
                UPDATE security_alerts 
                SET status = %s, updated_at = CURRENT_TIMESTAMP 
                WHERE alert_id = %s
            """, (status, alert_id))
            
            return result > 0
            
        except Exception as e:
            print(f"Error updating alert status: {e}")
            return False
    
    def get_alert_statistics(self) -> Dict[str, Any]:
        """Get alert statistics for dashboard."""
        try:
            stats = {}
            
            # Total alerts
            total_result = self.rds.execute_query("SELECT COUNT(*) FROM security_alerts")
            stats['total_alerts'] = total_result[0][0] if total_result else 0
            
            # Alerts by severity
            severity_result = self.rds.execute_query("""
                SELECT severity, COUNT(*) 
                FROM security_alerts 
                GROUP BY severity
            """)
            stats['by_severity'] = {row[0]: row[1] for row in severity_result} if severity_result else {}
            
            # Alerts by status
            status_result = self.rds.execute_query("""
                SELECT status, COUNT(*) 
                FROM security_alerts 
                GROUP BY status
            """)
            stats['by_status'] = {row[0]: row[1] for row in status_result} if status_result else {}
            
            # Recent alerts (last 24 hours)
            recent_result = self.rds.execute_query("""
                SELECT COUNT(*) 
                FROM security_alerts 
                WHERE timestamp > NOW() - INTERVAL '24 hours'
            """)
            stats['recent_24h'] = recent_result[0][0] if recent_result else 0
            
            return stats
            
        except Exception as e:
            print(f"Error getting statistics: {e}")
            return {
                'total_alerts': 0,
                'by_severity': {},
                'by_status': {},
                'recent_24h': 0
            }
    
    def health_check(self) -> Dict[str, Any]:
        """Check storage health."""
        try:
            # Test RDS connection
            rds_test = self.rds.execute_query("SELECT 1")
            rds_healthy = len(rds_test) > 0
            
            # Test DocumentDB connection
            docdb_test = self.documentdb.find_documents('security_investigations', {}, limit=1)
            docdb_healthy = isinstance(docdb_test, list)
            
            return {
                'status': 'healthy' if (rds_healthy and docdb_healthy) else 'degraded',
                'rds_connection': 'healthy' if rds_healthy else 'failed',
                'documentdb_connection': 'healthy' if docdb_healthy else 'failed',
                'storage_initialized': True
            }
            
        except Exception as e:
            return {
                'status': 'unhealthy',
                'error': str(e),
                'storage_initialized': False
            }