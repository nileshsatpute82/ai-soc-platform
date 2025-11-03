import os
import json
from sqlalchemy import create_engine, text
from pymongo import MongoClient
import redis
from typing import Dict, Any, Optional

class DataStorageComponent:
    def __init__(self):
        self.pg_engine = create_engine(os.getenv('DATABASE_URL'))
        self.mongo_client = MongoClient(os.getenv('MONGODB_URL'))
        self.mongo_db = self.mongo_client.get_default_database()
        self.redis_client = redis.from_url(os.getenv('REDIS_URL'))
    
    def store_data(self, data: Dict[str, Any], metadata: Dict[str, Any]) -> str:
        """Route data to appropriate storage based on type"""
        data_type = self._classify_data_type(data)
        
        if data_type == 'STRUCTURED':
            return self._store_relational(data, metadata)
        else:
            return self._store_document(data, metadata)
    
    def _classify_data_type(self, data: Dict[str, Any]) -> str:
        """Classify data as STRUCTURED or FLEXIBLE"""
        if isinstance(data, dict) and all(isinstance(v, (str, int, float, bool)) for v in data.values()):
            return 'STRUCTURED'
        return 'FLEXIBLE'
    
    def _store_relational(self, data: Dict[str, Any], metadata: Dict[str, Any]) -> str:
        """Store structured data in PostgreSQL"""
        with self.pg_engine.connect() as conn:
            result = conn.execute(
                text("INSERT INTO structured_data (data, metadata) VALUES (:data, :metadata) RETURNING id"),
                {"data": json.dumps(data), "metadata": json.dumps(metadata)}
            )
            return str(result.fetchone()[0])
    
    def _store_document(self, data: Dict[str, Any], metadata: Dict[str, Any]) -> str:
        """Store flexible data in MongoDB"""
        document = {"data": data, "metadata": metadata}
        result = self.mongo_db.flexible_data.insert_one(document)
        return str(result.inserted_id)
    
    def retrieve_data(self, data_id: str, storage_type: str) -> Optional[Dict[str, Any]]:
        """Retrieve data from appropriate storage"""
        if storage_type == 'STRUCTURED':
            return self._retrieve_relational(data_id)
        else:
            return self._retrieve_document(data_id)
    
    def _retrieve_relational(self, data_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve from PostgreSQL"""
        with self.pg_engine.connect() as conn:
            result = conn.execute(
                text("SELECT data, metadata FROM structured_data WHERE id = :id"),
                {"id": data_id}
            )
            row = result.fetchone()
            if row:
                return {"data": json.loads(row[0]), "metadata": json.loads(row[1])}
        return None
    
    def _retrieve_document(self, data_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve from MongoDB"""
        from bson import ObjectId
        document = self.mongo_db.flexible_data.find_one({"_id": ObjectId(data_id)})
        if document:
            return {"data": document["data"], "metadata": document["metadata"]}
        return None