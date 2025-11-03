# Infrastructure & Integration Unit - Infrastructure Design

## Infrastructure Mapping Overview
**Architecture**: Hybrid Render.com + AWS managed services approach
**Strategy**: Render for compute/application services, AWS for data and infrastructure services

## Compute Infrastructure (Render.com)

### Application Services
**Platform**: Render.com Web Services
**Configuration**:
- **Service Type**: Web Service with auto-scaling
- **Runtime**: Python 3.11 with Flask framework
- **Instance Type**: Standard instances with 1GB RAM, 0.5 CPU
- **Scaling**: Auto-scale 1-10 instances based on CPU/memory usage
- **Health Checks**: HTTP health check endpoints
- **Environment**: Separate services for staging and production

### Background Workers
**Platform**: Render.com Background Workers
**Configuration**:
- **Service Type**: Background Worker service
- **Runtime**: Python 3.11 with Celery
- **Instance Type**: Standard instances with 2GB RAM, 1 CPU
- **Scaling**: Auto-scale 1-5 workers based on queue depth
- **Queue Integration**: AWS SQS integration via boto3

### Static Assets
**Platform**: Render.com Static Site
**Configuration**:
- **Service Type**: Static Site for dashboard assets
- **CDN**: Render's built-in CDN for global distribution
- **Caching**: Browser caching with appropriate cache headers
- **Compression**: Automatic gzip compression

## Database Infrastructure (AWS Managed)

### Relational Database (PostgreSQL)
**Service**: AWS RDS PostgreSQL
**Configuration**:
- **Instance Class**: db.t3.medium (2 vCPU, 4GB RAM)
- **Multi-AZ**: Enabled for high availability
- **Storage**: 100GB GP2 with auto-scaling to 1TB
- **Backup**: 7-day automated backups with point-in-time recovery
- **Read Replicas**: 2 read replicas for read scaling
- **Security**: VPC security groups, encryption at rest
- **Monitoring**: Enhanced monitoring with CloudWatch

### Document Database (MongoDB)
**Service**: AWS DocumentDB (MongoDB-compatible)
**Configuration**:
- **Instance Class**: db.t3.medium (2 vCPU, 4GB RAM)
- **Cluster**: 3-node cluster with automatic failover
- **Storage**: Encrypted storage with automatic scaling
- **Backup**: Continuous backup with 35-day retention
- **Security**: VPC security groups, TLS encryption
- **Monitoring**: CloudWatch metrics and logs

## Caching Infrastructure (AWS ElastiCache)

### Redis Cluster
**Service**: AWS ElastiCache for Redis
**Configuration**:
- **Node Type**: cache.t3.micro (2 nodes for development, cache.t3.small for production)
- **Cluster Mode**: Enabled with 2 shards and 1 replica per shard
- **Multi-AZ**: Enabled for automatic failover
- **Backup**: Daily automated backups
- **Security**: VPC security groups, encryption in transit and at rest
- **Monitoring**: CloudWatch metrics for cache performance

## Message Queue Infrastructure (AWS SQS)

### Message Queues
**Service**: AWS SQS (Simple Queue Service)
**Queue Configuration**:

#### Critical Queue
- **Type**: FIFO Queue for ordered processing
- **Visibility Timeout**: 30 seconds
- **Message Retention**: 14 days
- **Dead Letter Queue**: Enabled with 3 max receives
- **Encryption**: Server-side encryption with AWS KMS

#### Standard Queue
- **Type**: Standard Queue for high throughput
- **Visibility Timeout**: 60 seconds
- **Message Retention**: 7 days
- **Dead Letter Queue**: Enabled with 5 max receives
- **Batch Processing**: Enabled for efficiency

#### Background Queue
- **Type**: Standard Queue for batch operations
- **Visibility Timeout**: 300 seconds (5 minutes)
- **Message Retention**: 3 days
- **Long Polling**: Enabled to reduce costs
- **Batch Size**: Up to 10 messages per batch

## Monitoring Infrastructure (AWS Managed)

### Application Monitoring
**Service**: AWS CloudWatch
**Configuration**:
- **Custom Metrics**: Application performance and business metrics
- **Log Groups**: Separate log groups for different service types
- **Dashboards**: Real-time operational dashboards
- **Alarms**: Automated alerting based on thresholds
- **Log Retention**: 30 days for application logs, 90 days for audit logs

### Distributed Tracing
**Service**: AWS X-Ray
**Configuration**:
- **Tracing**: End-to-end request tracing across services
- **Sampling**: 10% sampling rate for performance
- **Service Map**: Visual service dependency mapping
- **Integration**: Native integration with Render services via SDK

### Log Analytics
**Service**: AWS OpenSearch (formerly Elasticsearch)
**Configuration**:
- **Instance Type**: t3.small.search (1 vCPU, 2GB RAM)
- **Cluster**: 3-node cluster for high availability
- **Storage**: 20GB EBS storage per node
- **Index Management**: Automated index lifecycle management
- **Security**: Fine-grained access control with IAM integration

## Security Infrastructure

### Identity and Access Management
**Service**: AWS IAM
**Configuration**:
- **Service Roles**: Dedicated IAM roles for each Render service
- **Policies**: Least-privilege access policies
- **Cross-Account Access**: Secure access from Render to AWS services
- **Credential Management**: IAM roles with temporary credentials

### Secrets Management
**Service**: AWS Secrets Manager
**Configuration**:
- **Database Credentials**: Automatic rotation for database passwords
- **API Keys**: Secure storage for third-party API keys
- **Encryption**: KMS encryption for all secrets
- **Access Control**: IAM-based access control for secrets

### Network Security
**Service**: AWS VPC + Security Groups
**Configuration**:
- **VPC**: Dedicated VPC for all AWS resources
- **Subnets**: Private subnets for databases, public subnets for load balancers
- **Security Groups**: Restrictive security groups with minimal required access
- **NACLs**: Network ACLs for additional security layer

## AWS Service Integration

### Bedrock Integration
**Service**: AWS Bedrock
**Configuration**:
- **Model**: Claude 3.5 Sonnet
- **Access**: Direct API calls from Render services using IAM roles
- **Rate Limiting**: Application-level rate limiting to stay within service limits
- **Error Handling**: Circuit breaker pattern for resilience
- **Caching**: Response caching in ElastiCache for performance

### File Storage
**Service**: AWS S3
**Configuration**:
- **Buckets**: Separate buckets for different data types (logs, backups, artifacts)
- **Lifecycle Policies**: Automatic transition to IA and Glacier for cost optimization
- **Versioning**: Enabled for critical data protection
- **Encryption**: Server-side encryption with KMS keys
- **Access Control**: Bucket policies and IAM for secure access

### Configuration Management
**Service**: AWS Systems Manager Parameter Store
**Configuration**:
- **Parameters**: Environment-specific configuration parameters
- **Encryption**: SecureString parameters for sensitive configuration
- **Versioning**: Parameter versioning for rollback capability
- **Access Control**: IAM-based access control for parameters

## Networking and Connectivity

### Render to AWS Connectivity
**Method**: Public Internet with TLS encryption
**Configuration**:
- **Authentication**: IAM roles and temporary credentials
- **Encryption**: TLS 1.3 for all API communications
- **Rate Limiting**: Application-level rate limiting and retry logic
- **Monitoring**: CloudWatch metrics for API call monitoring

### Load Balancing
**Service**: Render's built-in load balancing
**Configuration**:
- **Health Checks**: HTTP health checks for service availability
- **SSL Termination**: Automatic SSL certificate management
- **Geographic Distribution**: Render's global edge network
- **Auto-scaling Integration**: Seamless integration with Render's auto-scaling

## Backup and Disaster Recovery

### Database Backups
**Strategy**: AWS managed backup services
**Configuration**:
- **RDS Backups**: Automated daily backups with 7-day retention
- **DocumentDB Backups**: Continuous backup with point-in-time recovery
- **Cross-Region Replication**: Backup replication to secondary AWS region
- **Recovery Testing**: Monthly disaster recovery testing

### Application Backups
**Strategy**: Configuration and code backup
**Configuration**:
- **Code Repository**: Git-based source control with GitHub
- **Configuration Backup**: Parameter Store and Secrets Manager replication
- **Infrastructure as Code**: Terraform/CDK for infrastructure reproducibility
- **Deployment Automation**: Automated deployment pipelines for quick recovery

## Cost Optimization

### Resource Right-Sizing
- **Development Environment**: Smaller instance sizes for cost efficiency
- **Production Environment**: Appropriately sized instances for performance requirements
- **Auto-Scaling**: Automatic scaling to optimize costs during low usage periods
- **Reserved Instances**: Reserved capacity for predictable workloads

### Storage Optimization
- **S3 Lifecycle Policies**: Automatic data tiering for cost optimization
- **Database Storage**: Auto-scaling storage to avoid over-provisioning
- **Log Retention**: Appropriate retention periods to balance compliance and cost
- **Monitoring**: Cost monitoring and alerting for budget management

## Performance Optimization

### Caching Strategy
- **Application Caching**: In-memory caching within Render services
- **Redis Caching**: Distributed caching for shared data
- **Database Caching**: Query result caching and connection pooling
- **CDN Caching**: Static asset caching via Render's CDN

### Database Performance
- **Read Replicas**: Read scaling for database queries
- **Connection Pooling**: Efficient database connection management
- **Query Optimization**: Automated query performance monitoring
- **Indexing Strategy**: Optimized indexing for common query patterns

This infrastructure design provides a robust, scalable, and cost-effective foundation for the AI-powered security operations platform while leveraging the strengths of both Render.com and AWS managed services.