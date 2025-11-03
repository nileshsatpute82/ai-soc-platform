"""AWS DocumentDB connection management with connection pooling."""

import boto3
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from typing import Dict, Any, Optional
from botocore.exceptions import ClientError

class DocumentDBClient:
    """AWS DocumentDB MongoDB client with connection management."""
    
    def __init__(self, config_service):
        self.config = config_service
        self.docdb = boto3.client(
            'docdb',
            region_name=self.config.get('AWS_REGION', 'us-east-1')
        )
        
        # MongoDB client
        self.mongo_client = None
        self.database = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize MongoDB client for DocumentDB."""
        try:
            connection_string = (
                f"mongodb://{self.config.get('DOCDB_USER')}:"
                f"{self.config.get('DOCDB_PASSWORD')}@"
                f"{self.config.get('DOCDB_HOST')}:"
                f"{self.config.get('DOCDB_PORT', '27017')}/"
                f"{self.config.get('DOCDB_DATABASE')}?"
                f"ssl=true&ssl_ca_certs=rds-ca-2019-root.pem&replicaSet=rs0&readPreference=secondaryPreferred"
            )
            
            self.mongo_client = MongoClient(
                connection_string,
                maxPoolSize=int(self.config.get('DOCDB_POOL_SIZE', '50')),
                serverSelectionTimeoutMS=int(self.config.get('DOCDB_TIMEOUT', '5000'))
            )
            
            self.database = self.mongo_client[self.config.get('DOCDB_DATABASE')]
            
        except Exception as e:
            raise Exception(f"Failed to initialize DocumentDB client: {str(e)}")
    
    def get_collection(self, collection_name: str):
        """Get MongoDB collection."""
        return self.database[collection_name]
    
    def insert_document(self, collection_name: str, document: Dict[str, Any]) -> str:
        """Insert document and return ID."""
        collection = self.get_collection(collection_name)
        result = collection.insert_one(document)
        return str(result.inserted_id)
    
    def find_documents(self, collection_name: str, query: Dict[str, Any] = None, limit: int = None) -> list:
        """Find documents matching query."""
        collection = self.get_collection(collection_name)
        cursor = collection.find(query or {})
        
        if limit:
            cursor = cursor.limit(limit)
            
        return list(cursor)
    
    def update_document(self, collection_name: str, query: Dict[str, Any], update: Dict[str, Any]) -> int:
        """Update documents and return modified count."""
        collection = self.get_collection(collection_name)
        result = collection.update_many(query, {"$set": update})
        return result.modified_count
    
    def delete_documents(self, collection_name: str, query: Dict[str, Any]) -> int:
        """Delete documents and return deleted count."""
        collection = self.get_collection(collection_name)
        result = collection.delete_many(query)
        return result.deleted_count
    
    def get_cluster_status(self, cluster_id: str) -> Dict[str, Any]:
        """Get DocumentDB cluster status."""
        try:
            response = self.docdb.describe_db_clusters(DBClusterIdentifier=cluster_id)
            cluster = response['DBClusters'][0]
            
            return {
                "status": cluster['Status'],
                "engine": cluster['Engine'],
                "engine_version": cluster['EngineVersion'],
                "endpoint": cluster.get('Endpoint'),
                "reader_endpoint": cluster.get('ReaderEndpoint'),
                "port": cluster.get('Port'),
                "availability_zones": cluster.get('AvailabilityZones', [])
            }
        except ClientError as e:
            return {"status": "error", "error": str(e)}
    
    def health_check(self) -> Dict[str, Any]:
        """Check DocumentDB connection health."""
        try:
            # Test connection with ping
            self.mongo_client.admin.command('ping')
            
            # Test database access
            collections = self.database.list_collection_names()
            
            return {
                "status": "healthy",
                "database": self.config.get('DOCDB_DATABASE'),
                "collections_count": len(collections),
                "connection": "active"
            }
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            return {
                "status": "unhealthy",
                "error": str(e),
                "connection": "failed"
            }
    
    def close_connection(self):
        """Close MongoDB client connection."""
        if self.mongo_client:
            self.mongo_client.close()