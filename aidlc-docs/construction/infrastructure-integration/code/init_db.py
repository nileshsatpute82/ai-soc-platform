#!/usr/bin/env python3
"""Database initialization script"""

import os
from models.database_manager import DatabaseManager

def init_databases():
    """Initialize all databases"""
    db_manager = DatabaseManager()
    
    print("Initializing PostgreSQL tables...")
    db_manager.init_postgresql_tables()
    
    print("Creating MongoDB collections...")
    # MongoDB collections are created automatically on first insert
    collections = [
        'flexible_data',
        'investigation_findings', 
        'ai_analysis_results',
        'mitre_mappings',
        'threat_intelligence'
    ]
    
    for collection in collections:
        db_manager.get_mongo_collection(collection)
        print(f"Collection '{collection}' ready")
    
    print("Database initialization complete!")
    
    # Health check
    health = db_manager.health_check()
    print("Database health check:")
    for db, status in health.items():
        print(f"  {db}: {status}")

if __name__ == "__main__":
    init_databases()