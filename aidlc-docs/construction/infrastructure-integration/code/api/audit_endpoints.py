"""Audit logging API endpoints."""

from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from typing import Dict, Any, List

audit_bp = Blueprint('audit', __name__, url_prefix='/api/audit')

class AuditEndpoints:
    """Audit logging API endpoints."""
    
    def __init__(self, audit_service):
        self.audit_service = audit_service
        self._register_routes()
    
    def _register_routes(self):
        """Register audit API routes."""
        
        @audit_bp.route('/events', methods=['POST'])
        def log_event():
            """Log audit event."""
            try:
                data = request.get_json()
                required_fields = ['event_type', 'severity']
                
                if not all(field in data for field in required_fields):
                    return jsonify({"status": "error", "error": "Missing required fields"}), 400
                
                event_id = self.audit_service.log_event(
                    event_type=data['event_type'],
                    severity=data['severity'],
                    details=data.get('details', {}),
                    user_id=data.get('user_id'),
                    session_id=data.get('session_id')
                )
                
                return jsonify({"status": "success", "event_id": event_id}), 201
            except Exception as e:
                return jsonify({"status": "error", "error": str(e)}), 500
        
        @audit_bp.route('/events', methods=['GET'])
        def get_events():
            """Get audit events with filtering."""
            try:
                # Query parameters
                event_type = request.args.get('event_type')
                severity = request.args.get('severity')
                user_id = request.args.get('user_id')
                start_date = request.args.get('start_date')
                end_date = request.args.get('end_date')
                limit = int(request.args.get('limit', 100))
                offset = int(request.args.get('offset', 0))
                
                # Build filters
                filters = {}
                if event_type:
                    filters['event_type'] = event_type
                if severity:
                    filters['severity'] = severity
                if user_id:
                    filters['user_id'] = user_id
                
                # Date range
                if start_date:
                    filters['start_date'] = datetime.fromisoformat(start_date)
                if end_date:
                    filters['end_date'] = datetime.fromisoformat(end_date)
                
                events = self.audit_service.get_events(
                    filters=filters,
                    limit=limit,
                    offset=offset
                )
                
                return jsonify({
                    "status": "success",
                    "events": events,
                    "count": len(events),
                    "limit": limit,
                    "offset": offset
                }), 200
                
            except Exception as e:
                return jsonify({"status": "error", "error": str(e)}), 500
        
        @audit_bp.route('/events/<event_id>', methods=['GET'])
        def get_event(event_id: str):
            """Get specific audit event."""
            try:
                event = self.audit_service.get_event_by_id(event_id)
                if not event:
                    return jsonify({"status": "error", "error": "Event not found"}), 404
                
                return jsonify({"status": "success", "event": event}), 200
            except Exception as e:
                return jsonify({"status": "error", "error": str(e)}), 500
        
        @audit_bp.route('/stats', methods=['GET'])
        def get_audit_stats():
            """Get audit statistics."""
            try:
                # Time range (default: last 24 hours)
                hours = int(request.args.get('hours', 24))
                start_time = datetime.utcnow() - timedelta(hours=hours)
                
                stats = self.audit_service.get_audit_statistics(start_time)
                
                return jsonify({"status": "success", "stats": stats}), 200
            except Exception as e:
                return jsonify({"status": "error", "error": str(e)}), 500
        
        @audit_bp.route('/export', methods=['GET'])
        def export_events():
            """Export audit events."""
            try:
                format_type = request.args.get('format', 'json')
                start_date = request.args.get('start_date')
                end_date = request.args.get('end_date')
                
                if not start_date or not end_date:
                    return jsonify({"status": "error", "error": "Start and end dates required"}), 400
                
                filters = {
                    'start_date': datetime.fromisoformat(start_date),
                    'end_date': datetime.fromisoformat(end_date)
                }
                
                export_data = self.audit_service.export_events(filters, format_type)
                
                return jsonify({
                    "status": "success",
                    "export_data": export_data,
                    "format": format_type
                }), 200
                
            except Exception as e:
                return jsonify({"status": "error", "error": str(e)}), 500