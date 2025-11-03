"""Health check endpoints for infrastructure monitoring."""

from flask import Blueprint, jsonify
from typing import Dict, Any
import time

health_bp = Blueprint('health', __name__, url_prefix='/health')

class HealthEndpoints:
    """Health check endpoints for all infrastructure components."""
    
    def __init__(self, app, aws_clients, components):
        self.app = app
        self.bedrock_client = aws_clients['bedrock']
        self.rds_client = aws_clients['rds']
        self.documentdb_client = aws_clients['documentdb']
        self.elasticache_client = aws_clients['elasticache']
        self.sqs_client = aws_clients['sqs']
        
        self.data_storage = components['data_storage']
        self.audit_service = components['audit_service']
        self.config_service = components['config_service']
        
        self._register_routes()
    
    def _register_routes(self):
        """Register health check routes."""
        
        @health_bp.route('/', methods=['GET'])
        def overall_health():
            """Overall system health check."""
            start_time = time.time()
            
            health_status = {
                "status": "healthy",
                "timestamp": time.time(),
                "components": {},
                "response_time_ms": 0
            }
            
            # Check all components
            components_to_check = [
                ("bedrock", self.bedrock_client.health_check),
                ("rds", self.rds_client.health_check),
                ("documentdb", self.documentdb_client.health_check),
                ("elasticache", self.elasticache_client.health_check),
                ("sqs", self.sqs_client.health_check),
                ("data_storage", self.data_storage.health_check),
                ("audit_service", self.audit_service.health_check),
                ("config_service", self.config_service.health_check)
            ]
            
            overall_healthy = True
            
            for component_name, health_func in components_to_check:
                try:
                    component_health = health_func()
                    health_status["components"][component_name] = component_health
                    
                    if component_health.get("status") != "healthy":
                        overall_healthy = False
                        
                except Exception as e:
                    health_status["components"][component_name] = {
                        "status": "error",
                        "error": str(e)
                    }
                    overall_healthy = False
            
            health_status["status"] = "healthy" if overall_healthy else "degraded"
            health_status["response_time_ms"] = round((time.time() - start_time) * 1000, 2)
            
            status_code = 200 if overall_healthy else 503
            return jsonify(health_status), status_code
        
        @health_bp.route('/bedrock', methods=['GET'])
        def bedrock_health():
            """AWS Bedrock service health."""
            try:
                health = self.bedrock_client.health_check()
                status_code = 200 if health.get("status") == "healthy" else 503
                return jsonify(health), status_code
            except Exception as e:
                return jsonify({"status": "error", "error": str(e)}), 503
        
        @health_bp.route('/database', methods=['GET'])
        def database_health():
            """Database services health (RDS + DocumentDB)."""
            try:
                rds_health = self.rds_client.health_check()
                docdb_health = self.documentdb_client.health_check()
                
                combined_health = {
                    "status": "healthy" if (rds_health.get("status") == "healthy" and 
                                         docdb_health.get("status") == "healthy") else "degraded",
                    "rds": rds_health,
                    "documentdb": docdb_health
                }
                
                status_code = 200 if combined_health["status"] == "healthy" else 503
                return jsonify(combined_health), status_code
                
            except Exception as e:
                return jsonify({"status": "error", "error": str(e)}), 503
        
        @health_bp.route('/cache', methods=['GET'])
        def cache_health():
            """ElastiCache Redis health."""
            try:
                health = self.elasticache_client.health_check()
                status_code = 200 if health.get("status") == "healthy" else 503
                return jsonify(health), status_code
            except Exception as e:
                return jsonify({"status": "error", "error": str(e)}), 503
        
        @health_bp.route('/queues', methods=['GET'])
        def queues_health():
            """SQS queues health."""
            try:
                health = self.sqs_client.health_check()
                status_code = 200 if health.get("status") in ["healthy", "partial"] else 503
                return jsonify(health), status_code
            except Exception as e:
                return jsonify({"status": "error", "error": str(e)}), 503
        
        @health_bp.route('/ready', methods=['GET'])
        def readiness_check():
            """Kubernetes readiness probe."""
            try:
                # Quick checks for critical components
                critical_checks = [
                    self.rds_client.health_check(),
                    self.config_service.health_check()
                ]
                
                ready = all(check.get("status") == "healthy" for check in critical_checks)
                
                return jsonify({
                    "ready": ready,
                    "timestamp": time.time()
                }), 200 if ready else 503
                
            except Exception as e:
                return jsonify({"ready": False, "error": str(e)}), 503
        
        @health_bp.route('/live', methods=['GET'])
        def liveness_check():
            """Kubernetes liveness probe."""
            return jsonify({
                "alive": True,
                "timestamp": time.time()
            }), 200