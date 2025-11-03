"""AWS ElastiCache Redis client with connection pooling."""

import boto3
import redis
from redis.connection import ConnectionPool
from typing import Dict, Any, Optional, Union
import json
from botocore.exceptions import ClientError

class ElastiCacheClient:
    """AWS ElastiCache Redis client with connection pooling."""
    
    def __init__(self, config_service):
        self.config = config_service
        self.elasticache = boto3.client(
            'elasticache',
            region_name=self.config.get('AWS_REGION', 'us-east-1')
        )
        
        # Redis connection pool
        self.redis_pool = None
        self.redis_client = None
        self._initialize_redis()
    
    def _initialize_redis(self):
        """Initialize Redis connection pool."""
        try:
            self.redis_pool = ConnectionPool(
                host=self.config.get('REDIS_HOST'),
                port=int(self.config.get('REDIS_PORT', '6379')),
                password=self.config.get('REDIS_PASSWORD'),
                db=int(self.config.get('REDIS_DB', '0')),
                max_connections=int(self.config.get('REDIS_POOL_SIZE', '50')),
                socket_timeout=int(self.config.get('REDIS_TIMEOUT', '5')),
                ssl=self.config.get('REDIS_SSL', 'true').lower() == 'true'
            )
            
            self.redis_client = redis.Redis(connection_pool=self.redis_pool)
            
        except Exception as e:
            raise Exception(f"Failed to initialize Redis client: {str(e)}")
    
    def set(self, key: str, value: Union[str, Dict, list], ttl: int = None) -> bool:
        """Set key-value with optional TTL."""
        try:
            if isinstance(value, (dict, list)):
                value = json.dumps(value)
            
            if ttl:
                return self.redis_client.setex(key, ttl, value)
            else:
                return self.redis_client.set(key, value)
        except Exception as e:
            raise Exception(f"Redis SET failed: {str(e)}")
    
    def get(self, key: str, as_json: bool = False) -> Optional[Union[str, Dict, list]]:
        """Get value by key with optional JSON parsing."""
        try:
            value = self.redis_client.get(key)
            if value is None:
                return None
            
            value = value.decode('utf-8')
            
            if as_json:
                try:
                    return json.loads(value)
                except json.JSONDecodeError:
                    return value
            
            return value
        except Exception as e:
            raise Exception(f"Redis GET failed: {str(e)}")
    
    def delete(self, *keys: str) -> int:
        """Delete keys and return count of deleted keys."""
        try:
            return self.redis_client.delete(*keys)
        except Exception as e:
            raise Exception(f"Redis DELETE failed: {str(e)}")
    
    def exists(self, key: str) -> bool:
        """Check if key exists."""
        try:
            return bool(self.redis_client.exists(key))
        except Exception as e:
            raise Exception(f"Redis EXISTS failed: {str(e)}")
    
    def increment(self, key: str, amount: int = 1) -> int:
        """Increment key value and return new value."""
        try:
            return self.redis_client.incrby(key, amount)
        except Exception as e:
            raise Exception(f"Redis INCREMENT failed: {str(e)}")
    
    def set_hash(self, key: str, mapping: Dict[str, Any]) -> bool:
        """Set hash fields."""
        try:
            # Convert values to strings
            string_mapping = {k: json.dumps(v) if isinstance(v, (dict, list)) else str(v) 
                            for k, v in mapping.items()}
            return self.redis_client.hset(key, mapping=string_mapping)
        except Exception as e:
            raise Exception(f"Redis HSET failed: {str(e)}")
    
    def get_hash(self, key: str, field: str = None) -> Union[Dict, str, None]:
        """Get hash field or entire hash."""
        try:
            if field:
                value = self.redis_client.hget(key, field)
                return value.decode('utf-8') if value else None
            else:
                hash_data = self.redis_client.hgetall(key)
                return {k.decode('utf-8'): v.decode('utf-8') for k, v in hash_data.items()}
        except Exception as e:
            raise Exception(f"Redis HGET failed: {str(e)}")
    
    def get_cache_cluster_status(self, cluster_id: str) -> Dict[str, Any]:
        """Get ElastiCache cluster status."""
        try:
            response = self.elasticache.describe_cache_clusters(
                CacheClusterId=cluster_id,
                ShowCacheNodeInfo=True
            )
            cluster = response['CacheClusters'][0]
            
            return {
                "status": cluster['CacheClusterStatus'],
                "engine": cluster['Engine'],
                "engine_version": cluster['EngineVersion'],
                "num_cache_nodes": cluster['NumCacheNodes'],
                "cache_node_type": cluster['CacheNodeType'],
                "availability_zone": cluster.get('PreferredAvailabilityZone'),
                "endpoint": cluster.get('RedisConfiguration', {}).get('PrimaryEndpoint', {}).get('Address') if cluster['Engine'] == 'redis' else None
            }
        except ClientError as e:
            return {"status": "error", "error": str(e)}
    
    def health_check(self) -> Dict[str, Any]:
        """Check Redis connection health."""
        try:
            # Test connection with ping
            ping_result = self.redis_client.ping()
            
            # Test basic operations
            test_key = "health_check_test"
            self.redis_client.set(test_key, "test_value", ex=10)
            test_value = self.redis_client.get(test_key)
            self.redis_client.delete(test_key)
            
            return {
                "status": "healthy",
                "ping": ping_result,
                "test_operation": "passed" if test_value == b"test_value" else "failed",
                "pool_size": self.redis_pool.max_connections if self.redis_pool else 0
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e)
            }
    
    def close_connection(self):
        """Close Redis connection pool."""
        if self.redis_client:
            self.redis_client.close()
        if self.redis_pool:
            self.redis_pool.disconnect()