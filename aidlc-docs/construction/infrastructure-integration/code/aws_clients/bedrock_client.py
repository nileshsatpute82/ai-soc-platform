"""AWS Bedrock client with circuit breaker pattern and caching."""

import boto3
import json
import time
from typing import Dict, Any
from functools import wraps
import redis
from botocore.exceptions import ClientError, BotoCoreError

class CircuitBreakerError(Exception):
    """Circuit breaker is open."""
    pass

class BedrockClient:
    """AWS Bedrock client with circuit breaker and caching."""
    
    def __init__(self, config_service):
        self.config = config_service
        self.bedrock = boto3.client(
            'bedrock-runtime',
            region_name=self.config.get('AWS_REGION', 'us-east-1')
        )
        self.redis_client = redis.Redis.from_url(
            self.config.get('REDIS_URL', 'redis://localhost:6379')
        )
        
        # Circuit breaker state
        self.failure_count = 0
        self.last_failure_time = 0
        self.circuit_open = False
        self.failure_threshold = int(self.config.get('CIRCUIT_BREAKER_THRESHOLD', '5'))
        self.recovery_timeout = int(self.config.get('CIRCUIT_BREAKER_TIMEOUT', '60'))
        
    def _circuit_breaker(self, func):
        """Circuit breaker decorator."""
        @wraps(func)
        def wrapper(*args, **kwargs):
            if self.circuit_open:
                if time.time() - self.last_failure_time > self.recovery_timeout:
                    self.circuit_open = False
                    self.failure_count = 0
                else:
                    raise CircuitBreakerError("Circuit breaker is open")
            
            try:
                result = func(*args, **kwargs)
                self.failure_count = 0
                return result
            except Exception as e:
                self.failure_count += 1
                self.last_failure_time = time.time()
                
                if self.failure_count >= self.failure_threshold:
                    self.circuit_open = True
                
                raise e
        return wrapper
    
    @_circuit_breaker
    def invoke_claude(self, prompt: str, model_id: str = "anthropic.claude-3-5-sonnet-20241022-v2:0") -> Dict[str, Any]:
        """Invoke Claude model with circuit breaker protection."""
        
        # Check cache first
        cache_key = f"bedrock:{model_id}:{hash(prompt)}"
        cached_result = self.redis_client.get(cache_key)
        if cached_result:
            return json.loads(cached_result)
        
        body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 4000,
            "messages": [{"role": "user", "content": prompt}]
        }
        
        try:
            response = self.bedrock.invoke_model(
                modelId=model_id,
                body=json.dumps(body),
                contentType='application/json'
            )
            
            result = json.loads(response['body'].read())
            
            # Cache result for 1 hour
            self.redis_client.setex(cache_key, 3600, json.dumps(result))
            
            return result
            
        except (ClientError, BotoCoreError) as e:
            raise Exception(f"Bedrock invocation failed: {str(e)}")
    
    def batch_invoke(self, prompts: list, model_id: str = "anthropic.claude-3-5-sonnet-20241022-v2:0") -> list:
        """Batch invoke multiple prompts with rate limiting."""
        results = []
        batch_delay = float(self.config.get('BEDROCK_BATCH_DELAY', '0.1'))
        
        for prompt in prompts:
            result = self.invoke_claude(prompt, model_id)
            results.append(result)
            time.sleep(batch_delay)
            
        return results
    
    def health_check(self) -> Dict[str, Any]:
        """Check Bedrock service health."""
        try:
            test_prompt = "Hello"
            self.invoke_claude(test_prompt)
            return {
                "status": "healthy",
                "circuit_open": self.circuit_open,
                "failure_count": self.failure_count
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e),
                "circuit_open": self.circuit_open,
                "failure_count": self.failure_count
            }