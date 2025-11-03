"""MITRE ATT&CK framework API endpoints."""

from flask import Blueprint, request, jsonify
from typing import Dict, Any, List

mitre_bp = Blueprint('mitre', __name__, url_prefix='/api/mitre')

class MitreEndpoints:
    """MITRE ATT&CK framework API endpoints."""
    
    def __init__(self, mitre_component, audit_service):
        self.mitre_component = mitre_component
        self.audit_service = audit_service
        self._register_routes()
    
    def _register_routes(self):
        """Register MITRE API routes."""
        
        @mitre_bp.route('/techniques', methods=['GET'])
        def get_techniques():
            """Get MITRE ATT&CK techniques."""
            try:
                tactic = request.args.get('tactic')
                platform = request.args.get('platform')
                
                techniques = self.mitre_component.get_techniques(tactic, platform)
                
                return jsonify({
                    "status": "success",
                    "techniques": techniques,
                    "count": len(techniques)
                }), 200
                
            except Exception as e:
                return jsonify({"status": "error", "error": str(e)}), 500
        
        @mitre_bp.route('/techniques/<technique_id>', methods=['GET'])
        def get_technique(technique_id: str):
            """Get specific MITRE technique."""
            try:
                technique = self.mitre_component.get_technique_by_id(technique_id)
                if not technique:
                    return jsonify({"status": "error", "error": "Technique not found"}), 404
                
                return jsonify({"status": "success", "technique": technique}), 200
            except Exception as e:
                return jsonify({"status": "error", "error": str(e)}), 500
        
        @mitre_bp.route('/tactics', methods=['GET'])
        def get_tactics():
            """Get MITRE ATT&CK tactics."""
            try:
                tactics = self.mitre_component.get_tactics()
                
                return jsonify({
                    "status": "success",
                    "tactics": tactics,
                    "count": len(tactics)
                }), 200
                
            except Exception as e:
                return jsonify({"status": "error", "error": str(e)}), 500
        
        @mitre_bp.route('/map', methods=['POST'])
        def map_indicators():
            """Map security indicators to MITRE techniques."""
            try:
                data = request.get_json()
                if not data or 'indicators' not in data:
                    return jsonify({"status": "error", "error": "Indicators required"}), 400
                
                mapping_result = self.mitre_component.map_to_mitre(data['indicators'])
                
                # Audit log
                self.audit_service.log_event(
                    event_type="mitre_mapping",
                    severity="low",
                    details={
                        "indicators_count": len(data['indicators']),
                        "mapped_techniques": len(mapping_result.get('techniques', [])),
                        "user": request.headers.get('X-User-ID', 'system')
                    }
                )
                
                return jsonify({
                    "status": "success",
                    "mapping": mapping_result
                }), 200
                
            except Exception as e:
                return jsonify({"status": "error", "error": str(e)}), 500
        
        @mitre_bp.route('/framework/update', methods=['POST'])
        def update_framework():
            """Update MITRE ATT&CK framework data."""
            try:
                force_update = request.args.get('force', 'false').lower() == 'true'
                
                update_result = self.mitre_component.update_framework(force_update)
                
                # Audit log
                self.audit_service.log_event(
                    event_type="mitre_framework_update",
                    severity="medium",
                    details={
                        "force_update": force_update,
                        "update_result": update_result,
                        "user": request.headers.get('X-User-ID', 'system')
                    }
                )
                
                return jsonify({
                    "status": "success",
                    "update_result": update_result
                }), 200
                
            except Exception as e:
                return jsonify({"status": "error", "error": str(e)}), 500
        
        @mitre_bp.route('/framework/status', methods=['GET'])
        def get_framework_status():
            """Get MITRE framework status."""
            try:
                status = self.mitre_component.get_framework_status()
                
                return jsonify({
                    "status": "success",
                    "framework_status": status
                }), 200
                
            except Exception as e:
                return jsonify({"status": "error", "error": str(e)}), 500
        
        @mitre_bp.route('/search', methods=['GET'])
        def search_techniques():
            """Search MITRE techniques."""
            try:
                query = request.args.get('q', '')
                if not query:
                    return jsonify({"status": "error", "error": "Search query required"}), 400
                
                results = self.mitre_component.search_techniques(query)
                
                return jsonify({
                    "status": "success",
                    "query": query,
                    "results": results,
                    "count": len(results)
                }), 200
                
            except Exception as e:
                return jsonify({"status": "error", "error": str(e)}), 500