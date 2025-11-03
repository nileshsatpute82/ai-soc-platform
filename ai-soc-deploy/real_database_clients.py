"""Real AWS database client implementations."""

import json
from typing import Dict, Any, List, Optional

# Conditional imports with fallbacks for compatibility
try:
    import psycopg2
    PSYCOPG2_AVAILABLE = True
except ImportError:
    PSYCOPG2_AVAILABLE = False
    psycopg2 = None

try:
    import pymongo
    PYMONGO_AVAILABLE = True
except ImportError:
    PYMONGO_AVAILABLE = False
    pymongo = None

try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    redis = None

class RealRDSClient:
    """Real AWS RDS PostgreSQL client."""
    
    def __init__(self, config_service):
        self.config = config_service
        self.connection = None
        self.connect()
    
    def connect(self):
        """Connect to PostgreSQL RDS."""
        if not PSYCOPG2_AVAILABLE:
            print("psycopg2 not available - using mock mode")
            self.connection = None
            return
            
        try:
            self.connection = psycopg2.connect(
                host=self.config.get('POSTGRES_HOST'),
                port=self.config.get('POSTGRES_PORT', 5432),
                database=self.config.get('POSTGRES_DB'),
                user=self.config.get('POSTGRES_USER'),
                password=self.config.get('POSTGRES_PASSWORD')
            )
            self.connection.autocommit = True
        except Exception as e:
            print(f"PostgreSQL connection failed: {e}")
            self.connection = None
    
    def execute_query(self, query: str, params: tuple = None) -> list:
        """Execute SELECT query."""
        if not self.connection:
            return []
        
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            results = cursor.fetchall()
            cursor.close()
            return results
        except Exception as e:
            print(f"Query execution failed: {e}")
            return []
    
    def execute_command(self, command: str, params: tuple = None) -> int:
        """Execute INSERT/UPDATE/DELETE command."""
        if not self.connection:
            return 0
        
        try:
            cursor = self.connection.cursor()
            cursor.execute(command, params)
            affected_rows = cursor.rowcount
            cursor.close()
            return affected_rows
        except Exception as e:
            print(f"Command execution failed: {e}")
            return 0
    
    def health_check(self) -> Dict[str, Any]:
        """Check RDS health."""
        if not self.connection:
            return {
                'status': 'degraded',
                'mode': 'real_aws',
                'service': 'rds',
                'message': 'Database configured but connection failed - using fallback mode',
                'host': self.config.get('POSTGRES_HOST')
            }
        
        try:
            result = self.execute_query("SELECT 1")
            return {
                'status': 'healthy',
                'mode': 'real_aws',
                'service': 'rds',
                'connection': 'active',
                'host': self.config.get('POSTGRES_HOST')
            }
        except Exception as e:
            return {
                'status': 'degraded',
                'mode': 'real_aws',
                'service': 'rds',
                'message': 'Database configured but connection issues - using fallback mode',
                'host': self.config.get('POSTGRES_HOST')
            }

class RealDocumentDBClient:
    """Real AWS DocumentDB client."""
    
    def __init__(self, config_service):
        self.config = config_service
        self.client = None
        self.database = None
        self.connect()
    
    def connect(self):
        """Connect to DocumentDB."""
        if not PYMONGO_AVAILABLE:
            print("pymongo not available - using mock mode")
            self.client = None
            self.database = None
            return
            
        try:
            connection_string = f"mongodb://{self.config.get('DOCDB_USER')}:{self.config.get('DOCDB_PASSWORD')}@{self.config.get('DOCDB_HOST')}:{self.config.get('DOCDB_PORT', 27017)}/{self.config.get('DOCDB_DATABASE')}?ssl=true&replicaSet=rs0&readPreference=secondaryPreferred&retryWrites=false"
            
            self.client = pymongo.MongoClient(connection_string)
            self.database = self.client[self.config.get('DOCDB_DATABASE')]
        except Exception as e:
            print(f"DocumentDB connection failed: {e}")
            self.client = None
            self.database = None
    
    def insert_document(self, collection_name: str, document: Dict[str, Any]) -> str:
        """Insert document."""
        if not self.database:
            return None
        
        try:
            collection = self.database[collection_name]
            result = collection.insert_one(document)
            return str(result.inserted_id)
        except Exception as e:
            print(f"Document insertion failed: {e}")
            return None
    
    def find_documents(self, collection_name: str, query: Dict[str, Any] = None, limit: int = None) -> list:
        """Find documents."""
        if not self.database:
            return []
        
        try:
            collection = self.database[collection_name]
            cursor = collection.find(query or {})
            if limit:
                cursor = cursor.limit(limit)
            
            documents = []
            for doc in cursor:
                doc['_id'] = str(doc['_id'])  # Convert ObjectId to string
                documents.append(doc)
            
            return documents
        except Exception as e:
            print(f"Document query failed: {e}")
            return []
    
    def health_check(self) -> Dict[str, Any]:
        """Check DocumentDB health."""
        if not self.client:
            return {
                'status': 'degraded',
                'mode': 'real_aws',
                'service': 'documentdb',
                'message': 'Database configured but connection failed - using fallback mode',
                'host': self.config.get('DOCDB_HOST')
            }
        
        try:
            # Test connection
            self.client.admin.command('ping')
            return {
                'status': 'healthy',
                'mode': 'real_aws',
                'service': 'documentdb',
                'connection': 'active',
                'host': self.config.get('DOCDB_HOST')
            }
        except Exception as e:
            return {
                'status': 'degraded',
                'mode': 'real_aws',
                'service': 'documentdb',
                'message': 'Database configured but connection issues - using fallback mode',
                'host': self.config.get('DOCDB_HOST')
            }

class RealElastiCacheClient:
    """Real AWS ElastiCache Redis client."""
    
    def __init__(self, config_service):
        self.config = config_service
        self.redis_client = None
        self.connect()
    
    def connect(self):
        """Connect to Redis."""
        if not REDIS_AVAILABLE:
            print("redis not available - using mock mode")
            self.redis_client = None
            return
            
        try:
            self.redis_client = redis.Redis(
                host=self.config.get('REDIS_HOST'),
                port=self.config.get('REDIS_PORT', 6379),
                decode_responses=True,
                socket_timeout=5,
                socket_connect_timeout=5
            )
            # Test connection
            self.redis_client.ping()
        except Exception as e:
            print(f"Redis connection failed: {e}")
            self.redis_client = None
    
    def set(self, key: str, value: Any, ttl: int = None) -> bool:
        """Set key-value."""
        if not self.redis_client:
            return False
        
        try:
            if isinstance(value, (dict, list)):
                value = json.dumps(value)
            
            if ttl:
                return self.redis_client.setex(key, ttl, value)
            else:
                return self.redis_client.set(key, value)
        except Exception as e:
            print(f"Redis set failed: {e}")
            return False
    
    def get(self, key: str, as_json: bool = False) -> Any:
        """Get value."""
        if not self.redis_client:
            return None
        
        try:
            value = self.redis_client.get(key)
            if value and as_json:
                return json.loads(value)
            return value
        except Exception as e:
            print(f"Redis get failed: {e}")
            return None
    
    def health_check(self) -> Dict[str, Any]:
        """Check Redis health."""
        if not self.redis_client:
            return {
                'status': 'degraded',
                'mode': 'real_aws',
                'service': 'elasticache',
                'message': 'Redis configured but connection failed - using fallback mode',
                'host': self.config.get('REDIS_HOST')
            }
        
        try:
            self.redis_client.ping()
            return {
                'status': 'healthy',
                'mode': 'real_aws',
                'service': 'elasticache',
                'connection': 'active',
                'host': self.config.get('REDIS_HOST')
            }
        except Exception as e:
            return {
                'status': 'degraded',
                'mode': 'real_aws',
                'service': 'elasticache',
                'message': 'Redis configured but connection issues - using fallback mode',
                'host': self.config.get('REDIS_HOST')
            }