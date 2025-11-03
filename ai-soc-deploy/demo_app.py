"""Demo Flask application with mock mode for immediate deployment."""

import os
from flask import Flask, jsonify, render_template
from mock_mode import (
    MockBedrockClient, MockRDSClient, MockDocumentDBClient,
    MockElastiCacheClient, MockSQSClient, MockConfigurationService,
    MockAuditService, MockMITREComponent
)
from core_platform import CorePlatformService
from aws_integration import create_aws_integrated_services
from real_alert_processor import RealAlertProcessor

def create_demo_app():
    """Create Flask application with AWS integration."""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'demo-secret-key')
    
    # Initialize AWS integrated services
    services = create_aws_integrated_services()
    
    config_service = services['config_service']
    audit_service = services['audit_service']
    aws_clients = services['aws_clients']
    mitre_component = services['mitre_component']
    aws_manager = services['aws_manager']
    
    # Core Platform Service
    core_platform = CorePlatformService(aws_clients['bedrock'], mitre_component, audit_service)
    
    # Real Alert Processor with database clients
    from real_database_clients import RealRDSClient, RealDocumentDBClient
    rds_client = aws_clients['rds'] if hasattr(aws_clients['rds'], 'connection') else None
    docdb_client = aws_clients['documentdb'] if hasattr(aws_clients['documentdb'], 'client') else None
    real_alerts = RealAlertProcessor(config_service, rds_client, docdb_client)
    
    @app.route('/')
    def home():
        """Security Operations Dashboard."""
        return render_template('prisma-dashboard.html')
    
    @app.route('/old-dashboard')
    def old_dashboard():
        """Original dark theme dashboard."""
        return render_template('dashboard.html')
    
    @app.route('/api/')
    def api_info():
        """API information endpoint."""
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
            "status": "running",
            "aws_integration": integration_status
        })
    
    @app.route('/health/')
    def health_check():
        """Overall system health check."""
        # Get integration status
        integration_status = aws_manager.get_integration_status()
        
        health_status = {
            "status": "healthy",
            "mode": integration_status["mode"],
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "aws_integration": integration_status,
            "real_alerts": real_alerts.health_check(),
            "components": {
                "bedrock": aws_clients['bedrock'].health_check(),
                "rds": aws_clients['rds'].health_check(),
                "documentdb": aws_clients['documentdb'].health_check(),
                "elasticache": aws_clients['elasticache'].health_check(),
                "sqs": aws_clients['sqs'].health_check(),
                "audit_service": audit_service.health_check(),
                "config_service": config_service.health_check(),
                "mitre_component": mitre_component.health_check()
            }
        }
        return jsonify(health_status)
    
    @app.route('/debug/rds')
    def debug_rds():
        """Debug RDS connection details."""
        try:
            debug_info = {
                'environment_variables': {
                    'POSTGRES_HOST': os.environ.get('POSTGRES_HOST', 'NOT_SET'),
                    'POSTGRES_USER': os.environ.get('POSTGRES_USER', 'NOT_SET'),
                    'POSTGRES_DB': os.environ.get('POSTGRES_DB', 'NOT_SET'),
                    'POSTGRES_PORT': os.environ.get('POSTGRES_PORT', 'NOT_SET'),
                    'ENABLE_REAL_DATABASES': os.environ.get('ENABLE_REAL_DATABASES', 'NOT_SET')
                },
                'config_service_values': {
                    'POSTGRES_HOST': config_service.get('POSTGRES_HOST'),
                    'POSTGRES_USER': config_service.get('POSTGRES_USER'),
                    'POSTGRES_DB': config_service.get('POSTGRES_DB'),
                    'POSTGRES_PORT': config_service.get('POSTGRES_PORT'),
                    'ENABLE_REAL_DATABASES': config_service.get('ENABLE_REAL_DATABASES')
                },
                'rds_client_type': type(aws_clients['rds']).__name__,
                'connection_test': None
            }
            
            # Test basic connection
            try:
                if hasattr(aws_clients['rds'], 'connection'):
                    if aws_clients['rds'].connection:
                        debug_info['connection_test'] = 'Connection object exists'
                    else:
                        debug_info['connection_test'] = 'Connection object is None'
                else:
                    debug_info['connection_test'] = 'No connection attribute'
            except Exception as e:
                debug_info['connection_test'] = f'Error testing connection: {str(e)}'
            
            return jsonify(debug_info)
            
        except Exception as e:
            return jsonify({
                'error': str(e),
                'timestamp': time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            }), 500
    
    @app.route('/debug/rds/test')
    def test_rds_query():
        """Test actual RDS query to see error."""
        try:
            result = aws_clients['rds'].execute_query("SELECT 1 as test")
            return jsonify({
                'status': 'success',
                'query_result': result,
                'connection_type': type(aws_clients['rds']).__name__
            })
        except Exception as e:
            return jsonify({
                'status': 'error',
                'error': str(e),
                'error_type': type(e).__name__,
                'connection_type': type(aws_clients['rds']).__name__
            }), 500
    
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
    
    @app.route('/api/alerts/process', methods=['POST'])
    def process_alert():
        """Process security alert through AI pipeline."""
        try:
            from flask import request
            alert_data = request.get_json() or {}
            
            # Use default demo alert if no data provided
            if not alert_data:
                alert_data = {
                    "alert_id": f"web_alert_{int(time.time())}",
                    "source": "Web_Interface",
                    "alert_type": "suspicious_activity",
                    "severity": "medium",
                    "description": "Suspicious activity detected via web interface",
                    "indicators": ["web_anomaly", "user_behavior"]
                }
            
            result = core_platform.process_security_alert(alert_data)
            return jsonify({"status": "success", "result": result})
            
        except Exception as e:
            return jsonify({"status": "error", "error": str(e)}), 500
    
    @app.route('/api/alerts/queue')
    def get_alert_queue():
        """Get current alert queue."""
        try:
            queue = core_platform.get_alert_queue()
            return jsonify({"status": "success", "alerts": queue, "count": len(queue)})
        except Exception as e:
            return jsonify({"status": "error", "error": str(e)}), 500
    
    @app.route('/api/crews/status')
    def get_crew_status():
        """Get AI crew status."""
        try:
            status = core_platform.get_crew_status()
            return jsonify({"status": "success", "crews": status})
        except Exception as e:
            return jsonify({"status": "error", "error": str(e)}), 500
    
    @app.route('/api/security/demo-alerts', methods=['POST'])
    def generate_demo_alerts():
        """Generate and process demo security alerts."""
        try:
            results = core_platform.generate_demo_alerts()
            return jsonify({
                "status": "success", 
                "message": f"Processed {len(results)} demo alerts",
                "alerts": results
            })
        except Exception as e:
            return jsonify({"status": "error", "error": str(e)}), 500
    
    @app.route('/api/alerts/')
    def get_real_alerts():
        """Get real security alerts from AWS SQS."""
        try:
            # Get real alerts from SQS
            real_aws_alerts = real_alerts.poll_alerts(max_messages=10)
            
            # Mock alerts for demo
            mock_alerts = [
                {
                    'alert_id': 'demo-001',
                    'timestamp': '2024-01-15T10:30:00Z',
                    'severity': 'HIGH',
                    'source': 'Demo Mode',
                    'description': 'Demo: Suspicious login from unusual location',
                    'event_type': 'Demo Alert'
                },
                {
                    'alert_id': 'demo-002', 
                    'timestamp': '2024-01-15T09:15:00Z',
                    'severity': 'MEDIUM',
                    'source': 'Demo Mode',
                    'description': 'Demo: Unusual network traffic detected',
                    'event_type': 'Demo Alert'
                }
            ]
            
            # Combine real and mock alerts
            all_alerts = real_aws_alerts + mock_alerts
            return jsonify({
                'alerts': all_alerts, 
                'real_alerts_count': len(real_aws_alerts),
                'total_count': len(all_alerts)
            })
        except Exception as e:
            return jsonify({"status": "error", "error": str(e)}), 500
    
    return app

if __name__ == '__main__':
    import time
    app = create_demo_app()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)