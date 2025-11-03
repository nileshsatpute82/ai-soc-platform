"""Demo Flask application with mock mode for immediate deployment."""

import os
from flask import Flask, jsonify
from mock_mode import (
    MockBedrockClient, MockRDSClient, MockDocumentDBClient,
    MockElastiCacheClient, MockSQSClient, MockConfigurationService,
    MockAuditService, MockMITREComponent
)

def create_demo_app():
    """Create demo Flask application with mock services."""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'demo-secret-key')
    
    # Initialize mock services
    config_service = MockConfigurationService()
    audit_service = MockAuditService(config_service)
    
    # Mock AWS clients
    bedrock_client = MockBedrockClient(config_service)
    rds_client = MockRDSClient(config_service)
    documentdb_client = MockDocumentDBClient(config_service)
    elasticache_client = MockElastiCacheClient(config_service)
    sqs_client = MockSQSClient(config_service)
    
    # Mock components
    mitre_component = MockMITREComponent(None, config_service)
    
    @app.route('/')
    def home():
        """Home page with API overview."""
        return jsonify({
            "name": "AI-Powered Security Operations Platform",
            "version": "1.0.0-demo",
            "mode": "mock",
            "description": "Infrastructure & Integration Unit - Demo Mode",
            "endpoints": {
                "health": "/health/",
                "config": "/api/config/",
                "audit": "/api/audit/events",
                "mitre": "/api/mitre/techniques",
                "demo": "/demo/"
            },
            "status": "running"
        })
    
    @app.route('/health/')
    def health_check():
        """Overall system health check."""
        health_status = {
            "status": "healthy",
            "mode": "mock",
            "timestamp": "2024-12-19T11:20:00Z",
            "components": {
                "bedrock": bedrock_client.health_check(),
                "rds": rds_client.health_check(),
                "documentdb": documentdb_client.health_check(),
                "elasticache": elasticache_client.health_check(),
                "sqs": sqs_client.health_check(),
                "audit_service": audit_service.health_check(),
                "config_service": config_service.health_check(),
                "mitre_component": mitre_component.health_check()
            }
        }
        return jsonify(health_status)
    
    @app.route('/api/config/')
    def get_config():
        """Get configuration."""
        return jsonify({
            "status": "success",
            "config": config_service.get_all_config()
        })
    
    @app.route('/api/audit/events')
    def get_audit_events():
        """Get audit events."""
        events = audit_service.get_events()
        return jsonify({
            "status": "success",
            "events": events,
            "count": len(events)
        })
    
    @app.route('/api/mitre/techniques')
    def get_mitre_techniques():
        """Get MITRE techniques."""
        techniques = mitre_component.get_techniques()
        return jsonify({
            "status": "success",
            "techniques": techniques,
            "count": len(techniques)
        })
    
    @app.route('/demo/')
    def demo_operations():
        """Demo security operations."""
        # Log demo event
        event_id = audit_service.log_event(
            event_type="demo_operation",
            severity="low",
            details={"action": "demo_security_analysis"}
        )
        
        # Mock AI analysis
        ai_response = bedrock_client.invoke_claude("Analyze security alert: suspicious login")
        
        # Mock MITRE mapping
        mitre_mapping = mitre_component.map_to_mitre(["suspicious_login", "failed_auth"])
        
        return jsonify({
            "demo": "AI Security Operations Platform",
            "operations": {
                "audit_event_logged": event_id,
                "ai_analysis": ai_response,
                "mitre_mapping": mitre_mapping
            },
            "message": "Demo operations completed successfully!"
        })
    
    return app

if __name__ == '__main__':
    app = create_demo_app()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)