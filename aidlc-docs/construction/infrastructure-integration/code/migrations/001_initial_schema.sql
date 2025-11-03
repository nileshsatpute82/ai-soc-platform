-- Initial PostgreSQL schema for AI SOC Infrastructure

-- Create structured_data table
CREATE TABLE IF NOT EXISTS structured_data (
    id SERIAL PRIMARY KEY,
    data JSONB NOT NULL,
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create audit_events table
CREATE TABLE IF NOT EXISTS audit_events (
    id SERIAL PRIMARY KEY,
    event_id VARCHAR(36) UNIQUE NOT NULL,
    event_type VARCHAR(50) NOT NULL,
    tier VARCHAR(20) NOT NULL,
    user_id VARCHAR(100),
    component VARCHAR(100),
    action VARCHAR(100),
    resource VARCHAR(200),
    result VARCHAR(20) NOT NULL,
    details JSONB,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    retention_expiry TIMESTAMP WITH TIME ZONE
);

-- Create configuration_items table
CREATE TABLE IF NOT EXISTS configuration_items (
    id SERIAL PRIMARY KEY,
    key VARCHAR(200) NOT NULL,
    value TEXT,
    environment VARCHAR(50) NOT NULL,
    component VARCHAR(100),
    is_secret BOOLEAN DEFAULT FALSE,
    version INTEGER DEFAULT 1,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create system_health_metrics table
CREATE TABLE IF NOT EXISTS system_health_metrics (
    id SERIAL PRIMARY KEY,
    component VARCHAR(100) NOT NULL,
    metric_name VARCHAR(100) NOT NULL,
    value VARCHAR(100) NOT NULL,
    unit VARCHAR(20),
    status VARCHAR(20) NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    tags JSONB
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_audit_events_timestamp ON audit_events(timestamp);
CREATE INDEX IF NOT EXISTS idx_audit_events_tier ON audit_events(tier);
CREATE INDEX IF NOT EXISTS idx_audit_events_event_type ON audit_events(event_type);
CREATE INDEX IF NOT EXISTS idx_config_items_key_env ON configuration_items(key, environment);
CREATE INDEX IF NOT EXISTS idx_health_metrics_component ON system_health_metrics(component);
CREATE INDEX IF NOT EXISTS idx_health_metrics_timestamp ON system_health_metrics(timestamp);