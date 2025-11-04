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
from real_services import RealAuditService, RealMITREComponent

def create_demo_app():
    """Create Flask application with AWS integration."""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'demo-secret-key')
    
    # Initialize AWS integrated services
    services = create_aws_integrated_services()
    
    config_service = services['config_service']
    aws_clients = services['aws_clients']
    aws_manager = services['aws_manager']
    
    # Use real services if RDS is available, otherwise fallback to mock
    if hasattr(aws_clients['rds'], 'execute_query'):
        audit_service = RealAuditService(aws_clients['rds'], config_service)
        mitre_component = RealMITREComponent(aws_clients['rds'], config_service)
    else:
        audit_service = services['audit_service']
        mitre_component = services['mitre_component']
    
    # Core Platform Service
    core_platform = CorePlatformService(aws_clients['bedrock'], mitre_component, audit_service)
    
    # Real Alert Processor with database clients
    real_alerts = RealAlertProcessor(config_service, aws_clients['rds'], aws_clients['documentdb'])
    
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
        """Get persistent security alerts from database + process new SQS alerts."""
        try:
            # Process new alerts from SQS (saves to database)
            new_alerts = real_alerts.poll_alerts(max_messages=10)
            
            # Get all stored alerts from database (persistent)
            stored_alerts = real_alerts.get_stored_alerts(limit=50)
            
            # Mock alerts for demo if no real alerts
            if not stored_alerts:
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
                stored_alerts = mock_alerts
            
            return jsonify({
                'alerts': stored_alerts, 
                'new_alerts_processed': len(new_alerts),
                'total_count': len(stored_alerts),
                'source': 'persistent_database'
            })
        except Exception as e:
            return jsonify({"status": "error", "error": str(e)}), 500
    
    @app.route('/api/alerts/stored')
    def get_stored_alerts():
        """Get alerts stored in PostgreSQL database."""
        try:
            stored_alerts = real_alerts.get_stored_alerts(limit=50)
            return jsonify({
                'status': 'success',
                'alerts': stored_alerts,
                'count': len(stored_alerts),
                'source': 'postgresql_database'
            })
        except Exception as e:
            return jsonify({"status": "error", "error": str(e)}), 500
    
    @app.route('/api/dashboard/metrics')
    def get_dashboard_metrics():
        """Get dashboard metrics from database."""
        try:
            if real_alerts.storage:
                metrics = real_alerts.storage.get_dashboard_metrics()
                return jsonify({
                    'status': 'success',
                    'metrics': metrics,
                    'source': 'database'
                })
            else:
                return jsonify({
                    'status': 'success',
                    'metrics': {'total_alerts': 0, 'high_priority_alerts': 0, 'resolved_incidents': 0, 'active_threats': 0},
                    'source': 'fallback'
                })
        except Exception as e:
            return jsonify({"status": "error", "error": str(e)}), 500
    
    @app.route('/api/dashboard/activity')
    def get_activity_timeline():
        """Get activity timeline from database."""
        try:
            if real_alerts.storage:
                activities = real_alerts.storage.get_activity_timeline(limit=20)
                return jsonify({
                    'status': 'success',
                    'activities': activities,
                    'source': 'database'
                })
            else:
                return jsonify({
                    'status': 'success',
                    'activities': [],
                    'source': 'fallback'
                })
        except Exception as e:
            return jsonify({"status": "error", "error": str(e)}), 500
    
    @app.route('/api/dashboard/mitre')
    def get_mitre_dashboard():
        """Get MITRE techniques from database."""
        try:
            if real_alerts.storage:
                techniques = real_alerts.storage.get_mitre_techniques()
                return jsonify({
                    'status': 'success',
                    'techniques': techniques,
                    'source': 'database'
                })
            else:
                return jsonify({
                    'status': 'success',
                    'techniques': [],
                    'source': 'fallback'
                })
        except Exception as e:
            return jsonify({"status": "error", "error": str(e)}), 500
    
    @app.route('/api/dashboard/charts')
    def get_chart_data():
        """Get chart data from database."""
        try:
            if real_alerts.storage:
                # Get alert statistics for charts
                stats = real_alerts.storage.get_alert_statistics()
                
                # Get recent alerts for timeline chart
                recent_alerts = real_alerts.storage.get_alerts(limit=100)
                
                # Process data for charts
                severity_data = stats.get('by_severity', {})
                status_data = stats.get('by_status', {})
                
                # Timeline data (alerts per day for last 7 days)
                from collections import defaultdict
                timeline_data = defaultdict(int)
                for alert in recent_alerts:
                    if alert.get('timestamp'):
                        date = alert['timestamp'][:10]  # Get date part
                        timeline_data[date] += 1
                
                return jsonify({
                    'status': 'success',
                    'charts': {
                        'severity_distribution': severity_data,
                        'status_distribution': status_data,
                        'timeline': dict(timeline_data),
                        'total_alerts': stats.get('total_alerts', 0)
                    },
                    'source': 'database'
                })
            else:
                return jsonify({
                    'status': 'success',
                    'charts': {
                        'severity_distribution': {},
                        'status_distribution': {},
                        'timeline': {},
                        'total_alerts': 0
                    },
                    'source': 'fallback'
                })
        except Exception as e:
            return jsonify({"status": "error", "error": str(e)}), 500
    
    @app.route('/api/dashboard/performance')
    def get_performance_metrics():
        """Get AI performance metrics from database."""
        try:
            if real_alerts.storage:
                metrics = real_alerts.storage.get_ai_performance_metrics()
                return jsonify({
                    'status': 'success',
                    'performance': metrics,
                    'source': 'database'
                })
            else:
                return jsonify({
                    'status': 'success',
                    'performance': {
                        'avg_response_time_ms': 1500,
                        'avg_accuracy': 0.92,
                        'active_crews': 3,
                        'total_processed_24h': 0
                    },
                    'source': 'fallback'
                })
        except Exception as e:
            return jsonify({"status": "error", "error": str(e)}), 500
    
    @app.route('/api/dashboard/mitre-stats')
    def get_mitre_stats():
        """Get MITRE technique statistics."""
        try:
            if hasattr(mitre_component, 'get_technique_stats'):
                stats = mitre_component.get_technique_stats()
                return jsonify({
                    'status': 'success',
                    'mitre_stats': stats,
                    'source': 'database'
                })
            else:
                return jsonify({
                    'status': 'success',
                    'mitre_stats': {
                        'total_techniques': 0,
                        'active_techniques': 0,
                        'top_tactic': 'Unknown',
                        'total_detections': 0
                    },
                    'source': 'fallback'
                })
        except Exception as e:
            return jsonify({"status": "error", "error": str(e)}), 500
    
    @app.route('/debug/database')
    def inspect_database():
        """Show all database tables and their contents."""
        try:
            db_data = {}
            
            # List of tables to inspect
            tables = [
                'security_alerts',
                'dashboard_metrics', 
                'activity_timeline',
                'mitre_techniques',
                'system_components'
            ]
            
            for table in tables:
                try:
                    # Get table structure
                    structure = aws_clients['rds'].execute_query(f"""
                        SELECT column_name, data_type 
                        FROM information_schema.columns 
                        WHERE table_name = '{table}'
                        ORDER BY ordinal_position
                    """)
                    
                    # Get table data (limit to 10 rows)
                    data = aws_clients['rds'].execute_query(f"SELECT * FROM {table} LIMIT 10")
                    
                    # Get row count
                    count_result = aws_clients['rds'].execute_query(f"SELECT COUNT(*) FROM {table}")
                    row_count = count_result[0][0] if count_result else 0
                    
                    db_data[table] = {
                        'structure': [{'column': col[0], 'type': col[1]} for col in structure] if structure else [],
                        'sample_data': data if data else [],
                        'total_rows': row_count,
                        'status': 'exists'
                    }
                    
                except Exception as e:
                    db_data[table] = {
                        'status': 'error',
                        'error': str(e)
                    }
            
            return jsonify({
                'status': 'success',
                'database': 'postgresql',
                'tables': db_data,
                'timestamp': time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            })
            
        except Exception as e:
            return jsonify({
                'status': 'error',
                'error': str(e),
                'timestamp': time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            }), 500
    
    return app

if __name__ == '__main__':
    import time
    app = create_demo_app()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)