"""Main Flask application with all API endpoints."""

from flask import Flask
from components import (
    DataStorageComponent, AWSBedrockIntegrationComponent, 
    MITREAttackMappingComponent, AuditService, ConfigurationService
)
from aws_clients import (
    BedrockClient, RDSClient, DocumentDBClient, 
    ElastiCacheClient, SQSClient
)
from api import (
    health_bp, HealthEndpoints,
    config_bp, ConfigEndpoints,
    audit_bp, AuditEndpoints,
    mitre_bp, MitreEndpoints
)

def create_app():
    """Create and configure Flask application."""
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = 'your-secret-key-here'
    
    # Initialize services
    config_service = ConfigurationService()
    audit_service = AuditService(config_service)
    
    # Initialize AWS clients
    aws_clients = {
        'bedrock': BedrockClient(config_service),
        'rds': RDSClient(config_service),
        'documentdb': DocumentDBClient(config_service),
        'elasticache': ElastiCacheClient(config_service),
        'sqs': SQSClient(config_service)
    }
    
    # Initialize components
    data_storage = DataStorageComponent(
        aws_clients['rds'], 
        aws_clients['documentdb'], 
        config_service
    )
    
    bedrock_integration = AWSBedrockIntegrationComponent(
        aws_clients['bedrock'],
        aws_clients['elasticache'],
        config_service
    )
    
    mitre_component = MITREAttackMappingComponent(
        data_storage,
        config_service
    )
    
    components = {
        'data_storage': data_storage,
        'bedrock_integration': bedrock_integration,
        'mitre_component': mitre_component,
        'audit_service': audit_service,
        'config_service': config_service
    }
    
    # Initialize API endpoints
    HealthEndpoints(app, aws_clients, components)
    ConfigEndpoints(config_service, audit_service)
    AuditEndpoints(audit_service)
    MitreEndpoints(mitre_component, audit_service)
    
    # Register blueprints
    app.register_blueprint(health_bp)
    app.register_blueprint(config_bp)
    app.register_blueprint(audit_bp)
    app.register_blueprint(mitre_bp)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=False)