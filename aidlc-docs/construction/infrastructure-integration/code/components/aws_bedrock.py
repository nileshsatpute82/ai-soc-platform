import boto3
import json
import time
import hashlib
from typing import Dict, Any, Optional
from datetime import datetime, timedelta

class CircuitBreaker:
    def __init__(self, failure_threshold: int = 5, timeout: int = 30):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = 'CLOSED'  # CLOSED, OPEN, HALF_OPEN
    
    def call(self, func, *args, **kwargs):
        if self.state == 'OPEN':
            if time.time() - self.last_failure_time > self.timeout:
                self.state = 'HALF_OPEN'
            else:
                raise Exception("Circuit breaker is OPEN")
        
        try:
            result = func(*args, **kwargs)
            if self.state == 'HALF_OPEN':
                self.state = 'CLOSED'
                self.failure_count = 0
            return result
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = time.time()
            if self.failure_count >= self.failure_threshold:
                self.state = 'OPEN'
            raise e

class AWSBedrockIntegrationComponent:
    def __init__(self):
        self.bedrock_client = boto3.client('bedrock-runtime')
        self.circuit_breaker = CircuitBreaker()
        self.cache = {}
        self.batch_requests = []
        self.batch_size = 10
    
    def invoke_claude(self, prompt: str, parameters: Dict[str, Any] = None) -> Dict[str, Any]:
        """Invoke Claude model with caching and circuit breaker"""
        cache_key = self._generate_cache_key(prompt, parameters)
        
        # Check cache first
        cached_response = self._get_cached_response(cache_key)
        if cached_response:
            return cached_response
        
        # Use circuit breaker for API call
        try:
            response = self.circuit_breaker.call(self._call_bedrock_api, prompt, parameters)
            self._cache_response(cache_key, response)
            return response
        except Exception as e:
            return {"error": str(e), "fallback": True}
    
    def _call_bedrock_api(self, prompt: str, parameters: Dict[str, Any] = None) -> Dict[str, Any]:
        """Direct API call to AWS Bedrock"""
        if parameters is None:
            parameters = {"max_tokens": 1000, "temperature": 0.1}
        
        body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": parameters.get("max_tokens", 1000),
            "temperature": parameters.get("temperature", 0.1),
            "messages": [{"role": "user", "content": prompt}]
        }
        
        response = self.bedrock_client.invoke_model(
            modelId="anthropic.claude-3-5-sonnet-20241022-v2:0",
            body=json.dumps(body)
        )
        
        response_body = json.loads(response['body'].read())
        return {
            "content": response_body['content'][0]['text'],
            "usage": response_body.get('usage', {}),
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def _generate_cache_key(self, prompt: str, parameters: Dict[str, Any]) -> str:
        """Generate cache key for request"""
        content = f"{prompt}:{json.dumps(parameters, sort_keys=True)}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def _get_cached_response(self, cache_key: str) -> Optional[Dict[str, Any]]:
        """Get cached response if valid"""
        if cache_key in self.cache:
            cached_item = self.cache[cache_key]
            if datetime.fromisoformat(cached_item['expires']) > datetime.utcnow():
                return cached_item['response']
            else:
                del self.cache[cache_key]
        return None
    
    def _cache_response(self, cache_key: str, response: Dict[str, Any]):
        """Cache response with TTL"""
        expires = datetime.utcnow() + timedelta(hours=1)
        self.cache[cache_key] = {
            'response': response,
            'expires': expires.isoformat()
        }