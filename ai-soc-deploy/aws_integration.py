"""Real AWS Integration - Production Mode"""

import os
import boto3
import json
from typing import Dict, Any, Optional
from botocore.exceptions import ClientError, NoCredentialsError
from mock_mode import (
    MockBedrockClient, MockRDSClient, MockDocumentDBClient,
    MockElastiCacheClient, MockSQSClient, MockConfigurationService,
    MockAuditService, MockMITREComponent
)
from real_aws_clients import (
    RealBedrockClient, RealSQSClient
)
# Conditional import for database clients
try:
    from real_database_clients import (
        RealRDSClient, RealDocumentDBClient, RealElastiCacheClient
    )
    DATABASE_CLIENTS_AVAILABLE = True
except ImportError as e:
    print(f"Database clients not available: {e}")
    DATABASE_CLIENTS_AVAILABLE = False
    RealRDSClient = None
    RealDocumentDBClient = None
    RealElastiCacheClient = None

class AWSIntegrationManager:
    """Manages switching between mock and real AWS services."""
    
    def __init__(self):
        self.use_real_aws = self._should_use_real_aws()
        self.aws_region = os.environ.get('AWS_REGION', 'us-east-1')
        
    def _should_use_real_aws(self) -> bool:
        """Determine if we should use real AWS services."""
        # Check if AWS credentials are available
        try:
            # Try to create a session to test credentials
            session = boto3.Session()
            credentials = session.get_credentials()
            
            if credentials is None:
                print("No AWS credentials found - using mock mode")
                return False
                
            # Check if user explicitly wants real AWS
            use_real = os.environ.get('USE_REAL_AWS', 'false').lower()
            if use_real in ['true', '1', 'yes']:
                print("Real AWS mode enabled via environment variable")
                return True
                
            # Check if Bedrock access key is provided
            if os.environ.get('AWS_ACCESS_KEY_ID') and os.environ.get('AWS_SECRET_ACCESS_KEY'):
                print("AWS credentials detected - real AWS mode available")
                return True
                
            return False
            
        except Exception as e:
            print(f"AWS credential check failed: {e} - using mock mode")
            return False
    
    def get_bedrock_client(self, config_service):
        """Get Bedrock client (real or mock)."""
        if self.use_real_aws:
            try:
                return RealBedrockClient(config_service)
            except Exception as e:
                print(f"Failed to create real Bedrock client: {e} - falling back to mock")
                return MockBedrockClient(config_service)
        else:
            return MockBedrockClient(config_service)
    
    def get_rds_client(self, config_service):
        """Get RDS client (real or mock)."""
        enable_real_dbs = config_service.get('ENABLE_REAL_DATABASES', 'false').lower() == 'true'
        if (DATABASE_CLIENTS_AVAILABLE and self.use_real_aws and 
            enable_real_dbs and self._has_rds_config()):
            try:
                return RealRDSClient(config_service)
            except Exception as e:
                print(f"Failed to create real RDS client: {e} - falling back to mock")
                return MockRDSClient(config_service)
        else:
            return MockRDSClient(config_service)
    
    def get_documentdb_client(self, config_service):
        """Get DocumentDB client (real or mock)."""
        enable_real_dbs = config_service.get('ENABLE_REAL_DATABASES', 'false').lower() == 'true'
        if (DATABASE_CLIENTS_AVAILABLE and self.use_real_aws and 
            enable_real_dbs and self._has_documentdb_config()):
            try:
                return RealDocumentDBClient(config_service)
            except Exception as e:
                print(f"Failed to create real DocumentDB client: {e} - falling back to mock")
                return MockDocumentDBClient(config_service)
        else:
            return MockDocumentDBClient(config_service)
    
    def get_elasticache_client(self, config_service):
        """Get ElastiCache client (real or mock)."""
        enable_real_dbs = config_service.get('ENABLE_REAL_DATABASES', 'false').lower() == 'true'
        if (DATABASE_CLIENTS_AVAILABLE and self.use_real_aws and 
            enable_real_dbs and self._has_redis_config()):
            try:
                return RealElastiCacheClient(config_service)
            except Exception as e:
                print(f"Failed to create real ElastiCache client: {e} - falling back to mock")
                return MockElastiCacheClient(config_service)
        else:
            return MockElastiCacheClient(config_service)
    
    def get_sqs_client(self, config_service):
        """Get SQS client (real or mock)."""
        if self.use_real_aws:
            try:
                return RealSQSClient(config_service)
            except Exception as e:
                print(f"Failed to create real SQS client: {e} - falling back to mock")
                return MockSQSClient(config_service)
        else:
            return MockSQSClient(config_service)
    
    def get_configuration_service(self):
        """Get configuration service (real or mock)."""
        if self.use_real_aws:
            try:
                return RealConfigurationService()
            except Exception as e:
                print(f"Failed to create real config service: {e} - falling back to mock")
                return MockConfigurationService()
        else:
            return MockConfigurationService()
    
    def _has_rds_config(self) -> bool:
        """Check if RDS configuration is available."""
        required = ['POSTGRES_HOST', 'POSTGRES_USER', 'POSTGRES_PASSWORD', 'POSTGRES_DB']
        return all(os.environ.get(key) for key in required)
    
    def _has_documentdb_config(self) -> bool:
        """Check if DocumentDB configuration is available."""
        required = ['DOCDB_HOST', 'DOCDB_USER', 'DOCDB_PASSWORD', 'DOCDB_DATABASE']
        return all(os.environ.get(key) for key in required)
    
    def _has_redis_config(self) -> bool:
        """Check if Redis configuration is available."""
        return bool(os.environ.get('REDIS_HOST'))
    
    def get_integration_status(self) -> Dict[str, Any]:
        """Get current integration status."""
        return {
            "mode": "real_aws" if self.use_real_aws else "mock",
            "aws_region": self.aws_region,
            "services": {
                "bedrock": "real" if self.use_real_aws else "mock",
                "rds": "real" if (self.use_real_aws and self._has_rds_config()) else "mock",
                "documentdb": "real" if (self.use_real_aws and self._has_documentdb_config()) else "mock",
                "elasticache": "real" if (self.use_real_aws and self._has_redis_config()) else "mock",
                "sqs": "real" if self.use_real_aws else "mock"
            },
            "credentials_available": bool(os.environ.get('AWS_ACCESS_KEY_ID')),
            "bedrock_enabled": self._check_bedrock_access()
        }
    
    def _check_bedrock_access(self) -> bool:
        """Check if Bedrock access is available."""
        if not self.use_real_aws:
            return False
            
        try:
            bedrock = boto3.client('bedrock', region_name=self.aws_region)
            # Try to list foundation models to test access
            bedrock.list_foundation_models()
            return True
        except Exception:
            return False

class RealConfigurationService:
    """Real configuration service using AWS Systems Manager Parameter Store."""
    
    def __init__(self):
        self.ssm = boto3.client('ssm', region_name=os.environ.get('AWS_REGION', 'us-east-1'))
        self.local_config = {
            "AWS_REGION": os.environ.get('AWS_REGION', 'us-east-1'),
            "USE_REAL_AWS": "true",
            "FLASK_ENV": os.environ.get('FLASK_ENV', 'production')
        }
    
    def get(self, key: str, default: str = None) -> str:
        """Get configuration value."""
        # First check environment variables
        env_value = os.environ.get(key)
        if env_value:
            return env_value
            
        # Then check local config
        if key in self.local_config:
            return self.local_config[key]
            
        # Finally check AWS Parameter Store (if available)
        try:
            parameter_name = f"/ai-soc/{key.lower()}"
            response = self.ssm.get_parameter(Name=parameter_name, WithDecryption=True)
            return response['Parameter']['Value']
        except Exception:
            return default
    
    def set(self, key: str, value: str):
        """Set configuration value."""
        self.local_config[key] = value
        
        # Optionally store in Parameter Store
        try:
            parameter_name = f"/ai-soc/{key.lower()}"
            self.ssm.put_parameter(
                Name=parameter_name,
                Value=value,
                Type='String',
                Overwrite=True
            )
        except Exception as e:
            print(f"Failed to store parameter in AWS: {e}")
    
    def get_all_config(self) -> Dict[str, str]:
        """Get all configuration."""
        config = self.local_config.copy()
        
        # Add environment variables
        for key, value in os.environ.items():
            if key.startswith(('AWS_', 'POSTGRES_', 'DOCDB_', 'REDIS_', 'FLASK_')):
                config[key] = value
                
        return config
    
    def health_check(self) -> Dict[str, Any]:
        """Health check for configuration service."""
        try:
            # Test Parameter Store access
            self.ssm.describe_parameters(MaxResults=1)
            return {"status": "healthy", "mode": "real", "parameter_store": "accessible"}
        except Exception as e:
            return {"status": "healthy", "mode": "real", "parameter_store": "unavailable", "error": str(e)}

def create_aws_integrated_services(config_service=None):
    """Create AWS integrated services based on availability."""
    
    # Initialize AWS integration manager
    aws_manager = AWSIntegrationManager()
    
    # Get configuration service
    if config_service is None:
        config_service = aws_manager.get_configuration_service()
    
    # Create AWS clients
    aws_clients = {
        'bedrock': aws_manager.get_bedrock_client(config_service),
        'rds': aws_manager.get_rds_client(config_service),
        'documentdb': aws_manager.get_documentdb_client(config_service),
        'elasticache': aws_manager.get_elasticache_client(config_service),
        'sqs': aws_manager.get_sqs_client(config_service)
    }
    
    # Create audit service (always use mock for now, can be enhanced later)
    audit_service = MockAuditService(config_service)
    
    # Create MITRE component
    mitre_component = MockMITREComponent(aws_clients['rds'], config_service)
    
    return {
        'aws_manager': aws_manager,
        'config_service': config_service,
        'aws_clients': aws_clients,
        'audit_service': audit_service,
        'mitre_component': mitre_component
    }