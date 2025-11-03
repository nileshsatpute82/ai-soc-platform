"""AWS RDS connection management with connection pooling."""

import boto3
import psycopg2
from psycopg2 import pool
from typing import Dict, Any, Optional
from contextlib import contextmanager
from botocore.exceptions import ClientError

class RDSClient:
    """AWS RDS PostgreSQL client with connection pooling."""
    
    def __init__(self, config_service):
        self.config = config_service
        self.rds = boto3.client(
            'rds',
            region_name=self.config.get('AWS_REGION', 'us-east-1')
        )
        
        # Connection pool
        self.connection_pool = None
        self._initialize_pool()
    
    def _initialize_pool(self):
        """Initialize PostgreSQL connection pool."""
        try:
            self.connection_pool = psycopg2.pool.ThreadedConnectionPool(
                minconn=int(self.config.get('DB_POOL_MIN', '2')),
                maxconn=int(self.config.get('DB_POOL_MAX', '20')),
                host=self.config.get('POSTGRES_HOST'),
                port=int(self.config.get('POSTGRES_PORT', '5432')),
                database=self.config.get('POSTGRES_DB'),
                user=self.config.get('POSTGRES_USER'),
                password=self.config.get('POSTGRES_PASSWORD'),
                sslmode='require'
            )
        except Exception as e:
            raise Exception(f"Failed to initialize RDS connection pool: {str(e)}")
    
    @contextmanager
    def get_connection(self):
        """Get connection from pool with context manager."""
        connection = None
        try:
            connection = self.connection_pool.getconn()
            yield connection
        except Exception as e:
            if connection:
                connection.rollback()
            raise e
        finally:
            if connection:
                self.connection_pool.putconn(connection)
    
    def execute_query(self, query: str, params: tuple = None) -> list:
        """Execute SELECT query and return results."""
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                return cursor.fetchall()
    
    def execute_command(self, command: str, params: tuple = None) -> int:
        """Execute INSERT/UPDATE/DELETE command and return affected rows."""
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(command, params)
                conn.commit()
                return cursor.rowcount
    
    def get_db_instance_status(self, instance_id: str) -> Dict[str, Any]:
        """Get RDS instance status."""
        try:
            response = self.rds.describe_db_instances(DBInstanceIdentifier=instance_id)
            instance = response['DBInstances'][0]
            
            return {
                "status": instance['DBInstanceStatus'],
                "engine": instance['Engine'],
                "engine_version": instance['EngineVersion'],
                "allocated_storage": instance['AllocatedStorage'],
                "availability_zone": instance['AvailabilityZone'],
                "endpoint": instance.get('Endpoint', {}).get('Address'),
                "port": instance.get('Endpoint', {}).get('Port')
            }
        except ClientError as e:
            return {"status": "error", "error": str(e)}
    
    def health_check(self) -> Dict[str, Any]:
        """Check RDS connection health."""
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT 1")
                    result = cursor.fetchone()
                    
            return {
                "status": "healthy",
                "pool_size": self.connection_pool.closed if self.connection_pool else 0,
                "test_query": "passed" if result and result[0] == 1 else "failed"
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e)
            }
    
    def close_pool(self):
        """Close all connections in the pool."""
        if self.connection_pool:
            self.connection_pool.closeall()