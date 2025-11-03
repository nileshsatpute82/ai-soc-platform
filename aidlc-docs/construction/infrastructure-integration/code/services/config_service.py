import boto3
import json
import os
from typing import Dict, Any, Optional, List
from datetime import datetime

class ConfigurationService:
    def __init__(self):
        self.ssm_client = boto3.client('ssm')
        self.environment = os.getenv('FLASK_ENV', 'development')
        self.config_cache = {}
        self.cache_ttl = 300  # 5 minutes
    
    def get_config(self, key: str, default: Any = None) -> Any:
        """Get configuration value with caching"""
        
        # Check cache first
        cached_value = self._get_from_cache(key)
        if cached_value is not None:
            return cached_value
        
        # Try environment variable first
        env_value = os.getenv(key)
        if env_value is not None:
            self._cache_value(key, env_value)
            return env_value
        
        # Try AWS Systems Manager Parameter Store
        ssm_value = self._get_from_ssm(key)
        if ssm_value is not None:
            self._cache_value(key, ssm_value)
            return ssm_value
        
        return default
    
    def set_config(self, key: str, value: Any, secure: bool = False) -> bool:
        """Set configuration value in Parameter Store"""
        try:
            parameter_name = f"/ai-soc-platform/{self.environment}/{key}"
            parameter_type = "SecureString" if secure else "String"
            
            # Validate configuration change
            if self._validate_config_change(key, value):
                self.ssm_client.put_parameter(
                    Name=parameter_name,
                    Value=str(value),
                    Type=parameter_type,
                    Overwrite=True,
                    Description=f"Configuration for {key} in {self.environment}"
                )
                
                # Update cache
                self._cache_value(key, value)
                
                # Log configuration change
                self._log_config_change(key, value, secure)
                
                return True
            return False
        except Exception as e:
            print(f"Error setting configuration {key}: {e}")
            return False
    
    def _get_from_ssm(self, key: str) -> Optional[Any]:
        """Get configuration from AWS Systems Manager"""
        try:
            parameter_name = f"/ai-soc-platform/{self.environment}/{key}"
            
            response = self.ssm_client.get_parameter(
                Name=parameter_name,
                WithDecryption=True
            )
            
            value = response['Parameter']['Value']
            
            # Try to parse as JSON, fallback to string
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return value
                
        except self.ssm_client.exceptions.ParameterNotFound:
            return None
        except Exception as e:
            print(f"Error getting parameter {key}: {e}")
            return None
    
    def _get_from_cache(self, key: str) -> Optional[Any]:
        """Get value from cache if not expired"""
        if key in self.config_cache:
            cached_item = self.config_cache[key]
            if datetime.utcnow().timestamp() - cached_item['timestamp'] < self.cache_ttl:
                return cached_item['value']
            else:
                del self.config_cache[key]
        return None
    
    def _cache_value(self, key: str, value: Any):
        """Cache configuration value"""
        self.config_cache[key] = {
            'value': value,
            'timestamp': datetime.utcnow().timestamp()
        }
    
    def _validate_config_change(self, key: str, value: Any) -> bool:
        """Validate configuration change"""
        
        # Define validation rules for specific keys
        validation_rules = {
            'CACHE_TTL': lambda v: isinstance(v, (int, str)) and int(v) > 0,
            'LOG_LEVEL': lambda v: v in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
            'CIRCUIT_BREAKER_THRESHOLD': lambda v: isinstance(v, (int, str)) and int(v) > 0
        }
        
        if key in validation_rules:
            try:
                return validation_rules[key](value)
            except Exception:
                return False
        
        # Default validation - non-empty string
        return value is not None and str(value).strip() != ""
    
    def _log_config_change(self, key: str, value: Any, secure: bool):
        """Log configuration change for audit"""
        # In a real implementation, this would use the AuditService
        print(f"Configuration changed: {key} = {'***' if secure else value}")
    
    def get_all_configs(self, prefix: str = None) -> Dict[str, Any]:
        """Get all configurations with optional prefix filter"""
        try:
            parameter_prefix = f"/ai-soc-platform/{self.environment}/"
            if prefix:
                parameter_prefix += prefix
            
            paginator = self.ssm_client.get_paginator('get_parameters_by_path')
            
            configs = {}
            for page in paginator.paginate(
                Path=parameter_prefix,
                Recursive=True,
                WithDecryption=True
            ):
                for parameter in page['Parameters']:
                    # Extract key from parameter name
                    key = parameter['Name'].replace(f"/ai-soc-platform/{self.environment}/", "")
                    
                    # Try to parse as JSON
                    try:
                        configs[key] = json.loads(parameter['Value'])
                    except json.JSONDecodeError:
                        configs[key] = parameter['Value']
            
            return configs
        except Exception as e:
            print(f"Error getting configurations: {e}")
            return {}
    
    def delete_config(self, key: str) -> bool:
        """Delete configuration parameter"""
        try:
            parameter_name = f"/ai-soc-platform/{self.environment}/{key}"
            
            self.ssm_client.delete_parameter(Name=parameter_name)
            
            # Remove from cache
            if key in self.config_cache:
                del self.config_cache[key]
            
            self._log_config_change(key, "DELETED", False)
            return True
        except Exception as e:
            print(f"Error deleting configuration {key}: {e}")
            return False