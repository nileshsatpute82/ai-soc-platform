"""Configuration management API endpoints."""

from flask import Blueprint, request, jsonify
from typing import Dict, Any

config_bp = Blueprint('config', __name__, url_prefix='/api/config')

class ConfigEndpoints:
    """Configuration management API endpoints."""
    
    def __init__(self, config_service, audit_service):
        self.config_service = config_service
        self.audit_service = audit_service
        self._register_routes()
    
    def _register_routes(self):
        """Register configuration API routes."""
        
        @config_bp.route('/', methods=['GET'])
        def get_all_config():
            """Get all configuration parameters."""
            try:
                config = self.config_service.get_all_config()
                return jsonify({"status": "success", "config": config}), 200
            except Exception as e:
                return jsonify({"status": "error", "error": str(e)}), 500
        
        @config_bp.route('/<key>', methods=['GET'])
        def get_config(key: str):
            """Get specific configuration parameter."""
            try:
                value = self.config_service.get(key)
                if value is None:
                    return jsonify({"status": "error", "error": "Key not found"}), 404
                
                return jsonify({"status": "success", "key": key, "value": value}), 200
            except Exception as e:
                return jsonify({"status": "error", "error": str(e)}), 500
        
        @config_bp.route('/<key>', methods=['PUT'])
        def update_config(key: str):
            """Update configuration parameter."""
            try:
                data = request.get_json()
                if not data or 'value' not in data:
                    return jsonify({"status": "error", "error": "Value required"}), 400
                
                old_value = self.config_service.get(key)
                self.config_service.set(key, data['value'])
                
                # Audit log
                self.audit_service.log_event(
                    event_type="config_update",
                    severity="medium",
                    details={
                        "key": key,
                        "old_value": old_value,
                        "new_value": data['value'],
                        "user": request.headers.get('X-User-ID', 'system')
                    }
                )
                
                return jsonify({"status": "success", "message": "Configuration updated"}), 200
            except Exception as e:
                return jsonify({"status": "error", "error": str(e)}), 500
        
        @config_bp.route('/reload', methods=['POST'])
        def reload_config():
            """Reload configuration from source."""
            try:
                self.config_service.reload_config()
                
                self.audit_service.log_event(
                    event_type="config_reload",
                    severity="low",
                    details={"user": request.headers.get('X-User-ID', 'system')}
                )
                
                return jsonify({"status": "success", "message": "Configuration reloaded"}), 200
            except Exception as e:
                return jsonify({"status": "error", "error": str(e)}), 500