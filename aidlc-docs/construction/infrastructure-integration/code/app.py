from flask import Flask
from flask_restx import Api
from components.data_storage import DataStorageComponent
from components.aws_bedrock import AWSBedrockIntegrationComponent
from components.mitre_mapping import MITREAttackMappingComponent
from services.audit_service import AuditService
from services.config_service import ConfigurationService
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')

api = Api(app, title='AI SOC Infrastructure API', version='1.0', description='Infrastructure and Integration Services')

# Initialize components
data_storage = DataStorageComponent()
bedrock_integration = AWSBedrockIntegrationComponent()
mitre_mapping = MITREAttackMappingComponent()
audit_service = AuditService()
config_service = ConfigurationService()

@app.route('/health')
def health_check():
    return {'status': 'healthy', 'service': 'ai-soc-infrastructure'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)))