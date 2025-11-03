# Infrastructure & Integration Unit - Deployment Architecture

## Deployment Overview
**Platform Strategy**: Hybrid Render.com + AWS architecture
**Deployment Model**: Multi-service deployment with managed infrastructure dependencies

## Render.com Deployment Architecture

### Service Deployment Structure
```
Render.com Platform
├── Web Services (Auto-scaling)
│   ├── API Gateway Service (Flask)
│   ├── Core Platform Service (Flask)
│   ├── Validation Service (Flask)
│   └── Health Check Service (Flask)
├── Background Workers (Auto-scaling)
│   ├── AI Processing Workers (Celery)
│   ├── Data Processing Workers (Celery)
│   └── Maintenance Workers (Celery)
├── Static Sites
│   ├── Dashboard Frontend (React/HTML/CSS/JS)
│   └── Documentation Site
└── Cron Jobs
    ├── Health Monitoring Jobs
    ├── Cleanup Jobs
    └── Backup Verification Jobs
```

### Environment Configuration

#### Production Environment
**Web Services**:
- **Instance Type**: Standard (1GB RAM, 0.5 CPU)
- **Auto-scaling**: 2-10 instances based on CPU >70% or Memory >80%
- **Health Checks**: `/health` endpoint with 30-second intervals
- **Environment Variables**: Production configuration via Render environment variables

**Background Workers**:
- **Instance Type**: Standard Plus (2GB RAM, 1 CPU)
- **Auto-scaling**: 1-5 workers based on SQS queue depth >50 messages
- **Queue Integration**: AWS SQS via boto3 SDK
- **Retry Logic**: Exponential backoff with 5 max retries

#### Staging Environment
**Web Services**:
- **Instance Type**: Starter (512MB RAM, 0.25 CPU)
- **Auto-scaling**: 1-3 instances
- **Health Checks**: Same as production with relaxed thresholds
- **Environment Variables**: Staging configuration with test data

**Background Workers**:
- **Instance Type**: Standard (1GB RAM, 0.5 CPU)
- **Auto-scaling**: 1-2 workers
- **Queue Integration**: Separate staging SQS queues
- **Testing**: Automated testing with mock AWS services

### Deployment Pipeline

#### CI/CD Workflow
```
GitHub Repository
├── Feature Branch → Pull Request
├── Staging Deployment (Automatic)
│   ├── Build & Test
│   ├── Security Scanning
│   ├── Deploy to Staging
│   └── Integration Tests
├── Production Deployment (Manual Approval)
│   ├── Build & Test
│   ├── Security Scanning
│   ├── Deploy to Production
│   └── Smoke Tests
└── Rollback (Automatic on Failure)
```

#### Build Configuration
**Dockerfile**:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```

**Build Settings**:
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn --bind 0.0.0.0:$PORT app:app`
- **Environment**: Python 3.11
- **Auto-Deploy**: Enabled for main branch

## AWS Infrastructure Deployment

### Regional Architecture
**Primary Region**: us-east-1 (N. Virginia)
**Secondary Region**: us-west-2 (Oregon) for disaster recovery

#### Multi-AZ Deployment
```
AWS us-east-1
├── Availability Zone 1a
│   ├── RDS Primary Instance
│   ├── DocumentDB Primary Node
│   └── ElastiCache Primary Node
├── Availability Zone 1b
│   ├── RDS Read Replica
│   ├── DocumentDB Secondary Node
│   └── ElastiCache Replica Node
└── Availability Zone 1c
    ├── RDS Read Replica
    ├── DocumentDB Secondary Node
    └── ElastiCache Replica Node
```

### Database Deployment Strategy

#### PostgreSQL (AWS RDS)
**Deployment Configuration**:
- **Engine**: PostgreSQL 15.x
- **Instance Class**: db.t3.medium (production), db.t3.micro (staging)
- **Multi-AZ**: Enabled for automatic failover
- **Storage**: 100GB GP2 with auto-scaling enabled
- **Backup Window**: 03:00-04:00 UTC (low traffic period)
- **Maintenance Window**: Sunday 04:00-05:00 UTC

**Connection Configuration**:
- **Connection Pooling**: PgBouncer with max 100 connections
- **SSL**: Required for all connections
- **Parameter Group**: Custom parameter group for performance optimization
- **Security Group**: Restricted access from Render IP ranges only

#### MongoDB (AWS DocumentDB)
**Deployment Configuration**:
- **Engine**: DocumentDB 4.0 (MongoDB-compatible)
- **Instance Class**: db.t3.medium (production), db.t3.small (staging)
- **Cluster**: 3-node cluster with automatic failover
- **Storage**: Encrypted with automatic scaling
- **Backup Window**: 02:00-03:00 UTC
- **Maintenance Window**: Sunday 03:00-04:00 UTC

### Caching Deployment (AWS ElastiCache)

#### Redis Configuration
**Production Cluster**:
- **Node Type**: cache.t3.small
- **Cluster Mode**: Enabled with 2 shards
- **Replication**: 1 replica per shard
- **Multi-AZ**: Enabled for automatic failover
- **Backup**: Daily automated backups at 01:00 UTC

**Staging Cluster**:
- **Node Type**: cache.t3.micro
- **Cluster Mode**: Disabled (single node)
- **Replication**: No replicas for cost optimization
- **Backup**: Weekly backups

### Message Queue Deployment (AWS SQS)

#### Queue Configuration
**Production Queues**:
- **Critical Queue**: FIFO queue with encryption
- **Standard Queue**: Standard queue with high throughput
- **Background Queue**: Standard queue with long polling
- **Dead Letter Queues**: Configured for all primary queues

**Staging Queues**:
- **Mirror Production**: Same configuration with reduced retention periods
- **Testing**: Additional test queues for integration testing

### Monitoring Deployment (AWS CloudWatch)

#### CloudWatch Configuration
**Log Groups**:
- `/render/api-gateway`: API gateway service logs
- `/render/core-platform`: Core platform service logs
- `/render/workers`: Background worker logs
- `/aws/rds/postgresql`: Database logs
- `/aws/documentdb/cluster`: DocumentDB logs

**Custom Metrics**:
- Application performance metrics
- Business logic metrics
- Security event metrics
- Resource utilization metrics

**Dashboards**:
- **Operational Dashboard**: Real-time system health
- **Business Dashboard**: Key performance indicators
- **Security Dashboard**: Security events and compliance

## Network Architecture

### Connectivity Model
```
Internet
    ↓
Render.com Platform (TLS 1.3)
    ↓
AWS API Gateway (HTTPS)
    ↓
AWS Services (VPC)
├── RDS (Private Subnet)
├── DocumentDB (Private Subnet)
├── ElastiCache (Private Subnet)
└── SQS (Managed Service)
```

### Security Configuration
**Network Security**:
- **VPC**: Dedicated VPC for all AWS resources
- **Subnets**: Private subnets for databases, public subnets for NAT gateways
- **Security Groups**: Restrictive rules allowing only necessary traffic
- **NACLs**: Additional network-level security controls

**Access Control**:
- **IAM Roles**: Service-specific roles with minimal permissions
- **API Keys**: Secure API key management via AWS Secrets Manager
- **Encryption**: TLS 1.3 for all communications, AES-256 for data at rest

## Deployment Automation

### Infrastructure as Code
**Terraform Configuration**:
```hcl
# AWS Provider
provider "aws" {
  region = var.aws_region
}

# VPC and Networking
module "vpc" {
  source = "./modules/vpc"
  cidr_block = "10.0.0.0/16"
}

# RDS PostgreSQL
module "postgresql" {
  source = "./modules/rds"
  engine = "postgres"
  instance_class = var.db_instance_class
}

# DocumentDB
module "documentdb" {
  source = "./modules/documentdb"
  cluster_size = 3
  instance_class = var.docdb_instance_class
}

# ElastiCache Redis
module "redis" {
  source = "./modules/elasticache"
  node_type = var.redis_node_type
  num_cache_nodes = 2
}
```

### Deployment Scripts
**Render Deployment**:
```bash
#!/bin/bash
# Deploy to Render.com
render-cli deploy --service api-gateway --branch main
render-cli deploy --service core-platform --branch main
render-cli deploy --service workers --branch main
render-cli deploy --service frontend --branch main
```

**AWS Infrastructure Deployment**:
```bash
#!/bin/bash
# Deploy AWS infrastructure
terraform init
terraform plan -var-file="production.tfvars"
terraform apply -var-file="production.tfvars"
```

## Scaling and Performance

### Auto-Scaling Configuration
**Render Services**:
- **Scale-Up Triggers**: CPU >70%, Memory >80%, Response Time >2s
- **Scale-Down Triggers**: CPU <30%, Memory <50%, Response Time <500ms
- **Scaling Policies**: Fast scale-up (1 minute), slow scale-down (5 minutes)

**AWS Services**:
- **RDS**: Read replica auto-scaling based on CPU and connection count
- **ElastiCache**: Cluster scaling based on memory usage and cache hit ratio
- **SQS**: No scaling required (managed service)

### Performance Optimization
**Caching Strategy**:
- **Application Level**: In-memory caching with 5-minute TTL
- **Redis Level**: Distributed caching with 1-hour TTL
- **Database Level**: Query result caching and connection pooling

**Database Optimization**:
- **Read Replicas**: Automatic read traffic distribution
- **Connection Pooling**: Efficient connection management
- **Query Optimization**: Automated performance insights and recommendations

## Disaster Recovery

### Backup Strategy
**Automated Backups**:
- **RDS**: Daily automated backups with 7-day retention
- **DocumentDB**: Continuous backup with point-in-time recovery
- **ElastiCache**: Daily snapshots with 5-day retention
- **Application Code**: Git repository with multiple remotes

### Recovery Procedures
**RTO (Recovery Time Objective)**: 15 minutes
**RPO (Recovery Point Objective)**: 5 minutes

**Failover Process**:
1. **Detection**: Automated health checks detect failure
2. **Notification**: Immediate alerts to operations team
3. **Failover**: Automatic database failover to secondary AZ
4. **Verification**: Automated smoke tests verify system functionality
5. **Communication**: Status updates to stakeholders

### Cross-Region Disaster Recovery
**Secondary Region Setup**:
- **Database Replicas**: Cross-region read replicas for major databases
- **Backup Replication**: Automated backup replication to secondary region
- **Infrastructure Code**: Terraform configurations for rapid deployment
- **Runbook**: Documented procedures for regional failover

This deployment architecture provides a robust, scalable, and maintainable foundation for the AI-powered security operations platform while optimizing for both performance and cost-effectiveness.