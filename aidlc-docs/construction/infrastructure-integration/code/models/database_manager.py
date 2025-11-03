import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pymongo import MongoClient
from models.postgresql_models import Base
import redis

class DatabaseManager:
    def __init__(self):
        # PostgreSQL setup
        self.pg_engine = create_engine(os.getenv('DATABASE_URL'))
        self.pg_session = sessionmaker(bind=self.pg_engine)
        
        # MongoDB setup
        self.mongo_client = MongoClient(os.getenv('MONGODB_URL'))
        self.mongo_db = self.mongo_client.get_default_database()
        
        # Redis setup
        self.redis_client = redis.from_url(os.getenv('REDIS_URL'))
    
    def init_postgresql_tables(self):
        """Initialize PostgreSQL tables"""
        Base.metadata.create_all(self.pg_engine)
    
    def get_pg_session(self):
        """Get PostgreSQL session"""
        return self.pg_session()
    
    def get_mongo_collection(self, collection_name: str):
        """Get MongoDB collection"""
        return self.mongo_db[collection_name]
    
    def get_redis_client(self):
        """Get Redis client"""
        return self.redis_client
    
    def health_check(self) -> dict:
        """Check health of all database connections"""
        health = {}
        
        # PostgreSQL health check
        try:
            with self.pg_engine.connect() as conn:
                conn.execute("SELECT 1")
            health['postgresql'] = 'healthy'
        except Exception as e:
            health['postgresql'] = f'unhealthy: {str(e)}'
        
        # MongoDB health check
        try:
            self.mongo_client.admin.command('ping')
            health['mongodb'] = 'healthy'
        except Exception as e:
            health['mongodb'] = f'unhealthy: {str(e)}'
        
        # Redis health check
        try:
            self.redis_client.ping()
            health['redis'] = 'healthy'
        except Exception as e:
            health['redis'] = f'unhealthy: {str(e)}'
        
        return health