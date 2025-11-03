# Shared Infrastructure Components

## Overview
Shared infrastructure components used across all units of the AI-powered security operations platform.

## AWS Shared Services

### Identity and Access Management (IAM)
**Purpose**: Centralized authentication and authorization for all units
**Shared Components**:
- **Service Roles**: Dedicated IAM roles for each unit's Render services
- **Cross-Service Policies**: Policies allowing inter-unit communication
- **User Management**: Centralized user authentication for analyst access
- **API Access**: Secure API access patterns for all units

**Role Structure**:
```
AI-SOC-Platform-Roles/
├── Infrastructure-Integration-Role
├── Core-Platform-Role
├── AI-Crew-Network-Role
├── AI-Crew-Endpoint-Role
├── AI-Crew-Cloud-Role
├── AI-Crew-ThreatIntel-Role
├── Frontend-Dashboard-Role
└── Backend-Validation-Role
```

### AWS Bedrock (Shared AI Service)
**Purpose**: Centralized AI processing for all AI crew units
**Shared Configuration**:
- **Model**: Claude 3.5 Sonnet (shared across all AI crews)
- **Rate Limiting**: Centralized rate limiting and quota management
- **Cost Management**: Shared billing and cost allocation
- **Performance Monitoring**: Unified monitoring across all AI requests

**Usage Patterns**:
- **Core Platform**: Alert triage and investigation orchestration
- **AI Crews**: Domain-specific threat analysis
- **Explanation Engine**: Plain-English threat explanations
- **Validation Service**: AI-assisted validation workflows

### Secrets Management (AWS Secrets Manager)
**Purpose**: Centralized secrets storage for all units
**Shared Secrets**:
- **Database Credentials**: PostgreSQL and MongoDB connection strings
- **API Keys**: Third-party service API keys
- **Encryption Keys**: Application-level encryption keys
- **Service Tokens**: Inter-service authentication tokens

**Access Patterns**:
- **Unit-Specific Secrets**: Each unit has access only to required secrets
- **Shared Secrets**: Common secrets accessible by multiple units
- **Rotation Policies**: Automated rotation for all database credentials
- **Audit Logging**: All secret access logged for compliance

### Configuration Management (AWS Systems Manager)
**Purpose**: Centralized configuration for all units
**Shared Parameters**:
- **Environment Configuration**: Environment-specific settings
- **Feature Flags**: System-wide feature toggles
- **Performance Tuning**: Shared performance parameters
- **Integration Settings**: External service integration configuration

**Parameter Hierarchy**:
```
/ai-soc-platform/
├── /global/
│   ├── /database/
│   ├── /cache/
│   └── /monitoring/
├── /environment/
│   ├── /production/
│   └── /staging/
└── /unit-specific/
    ├── /infrastructure/
    ├── /core-platform/
    └── /ai-crews/
```

## Database Shared Infrastructure

### PostgreSQL (AWS RDS) - Shared Relational Database
**Purpose**: Centralized structured data storage for all units
**Shared Schema Design**:

#### Core Tables (Used by Multiple Units)
- **users**: Analyst user accounts and profiles
- **alerts**: Security alerts from all sources
- **investigations**: Investigation records and status
- **audit_events**: System-wide audit trail
- **configurations**: System configuration settings

#### Unit-Specific Schemas
- **infrastructure_schema**: Infrastructure and integration data
- **core_platform_schema**: Core platform operational data
- **ai_crews_schema**: AI crew analysis results
- **frontend_schema**: Dashboard and UI state data
- **validation_schema**: Human validation workflows

**Access Control**:
- **Unit-Specific Users**: Each unit has dedicated database users
- **Schema Permissions**: Units have access only to required schemas
- **Shared Table Access**: Controlled access to shared tables via views
- **Audit Logging**: All database access logged for compliance

### MongoDB (AWS DocumentDB) - Shared Document Database
**Purpose**: Flexible data storage for investigation findings and AI analysis
**Shared Collections**:

#### Cross-Unit Collections
- **investigation_findings**: Investigation results from all units
- **ai_analysis_results**: AI analysis outputs from all crews
- **threat_intelligence**: Shared threat intelligence data
- **mitre_mappings**: MITRE ATT&CK framework mappings

#### Unit-Specific Collections
- **infrastructure_logs**: Infrastructure operational logs
- **core_platform_events**: Core platform event data
- **ai_crew_models**: AI crew-specific model data
- **validation_workflows**: Human validation process data

**Access Patterns**:
- **Read-Heavy Workloads**: Investigation data queries across units
- **Write-Heavy Workloads**: Real-time AI analysis result storage
- **Cross-Unit Queries**: Investigation correlation across multiple units
- **Data Retention**: Automated cleanup based on data age and compliance

## Caching Shared Infrastructure

### Redis Cluster (AWS ElastiCache) - Shared Cache
**Purpose**: High-performance caching for all units
**Shared Cache Namespaces**:

#### Global Cache Keys
- **mitre:**: MITRE ATT&CK framework data (shared across all units)
- **config:**: System configuration cache (shared)
- **users:**: User session and profile cache (shared)
- **threats:**: Threat intelligence cache (shared)

#### Unit-Specific Cache Keys
- **infra:**: Infrastructure component cache
- **core:**: Core platform operational cache
- **ai:network:**: Network AI crew cache
- **ai:endpoint:**: Endpoint AI crew cache
- **ai:cloud:**: Cloud AI crew cache
- **ai:threat:**: Threat intelligence AI crew cache
- **frontend:**: Dashboard and UI cache
- **validation:**: Validation workflow cache

**Cache Policies**:
- **TTL Management**: Different TTL policies for different data types
- **Eviction Policies**: LRU eviction for memory management
- **Cache Warming**: Proactive cache population for critical data
- **Invalidation**: Event-driven cache invalidation across units

## Message Queue Shared Infrastructure

### AWS SQS - Shared Message Queues
**Purpose**: Asynchronous communication between units
**Shared Queue Architecture**:

#### Inter-Unit Communication Queues
- **core-to-ai-crews**: Core platform to AI crew task distribution
- **ai-crews-to-core**: AI crew results back to core platform
- **validation-requests**: Validation requests from any unit
- **audit-events**: System-wide audit event queue

#### Unit-Specific Queues
- **infrastructure-tasks**: Infrastructure maintenance tasks
- **core-platform-tasks**: Core platform processing tasks
- **ai-crew-tasks**: AI-specific processing tasks
- **frontend-tasks**: Dashboard update tasks
- **validation-tasks**: Human validation workflow tasks

**Queue Policies**:
- **Message Routing**: Intelligent routing based on message type
- **Priority Handling**: Priority queues for critical security alerts
- **Dead Letter Queues**: Failed message handling for all queues
- **Batch Processing**: Efficient batch processing for high-volume operations

## Monitoring Shared Infrastructure

### AWS CloudWatch - Shared Monitoring
**Purpose**: Centralized monitoring and alerting for all units
**Shared Monitoring Components**:

#### Cross-Unit Metrics
- **System Performance**: Overall platform performance metrics
- **Security Events**: Security-related events from all units
- **Business Metrics**: Key performance indicators across units
- **Cost Metrics**: Resource usage and cost tracking

#### Shared Dashboards
- **Executive Dashboard**: High-level platform health and KPIs
- **Operations Dashboard**: Detailed operational metrics
- **Security Dashboard**: Security events and compliance status
- **Performance Dashboard**: System performance and optimization

**Alerting Strategy**:
- **Critical Alerts**: Immediate notification for system-wide issues
- **Warning Alerts**: Proactive alerts for potential issues
- **Business Alerts**: Alerts for business metric thresholds
- **Security Alerts**: Real-time security event notifications

### AWS X-Ray - Shared Distributed Tracing
**Purpose**: End-to-end request tracing across all units
**Tracing Configuration**:
- **Service Map**: Visual representation of inter-unit communication
- **Performance Analysis**: Latency analysis across unit boundaries
- **Error Tracking**: Error propagation tracking across units
- **Bottleneck Identification**: Performance bottleneck detection

## Security Shared Infrastructure

### Network Security (AWS VPC)
**Purpose**: Shared network security for all AWS resources
**VPC Configuration**:
- **Shared VPC**: Single VPC for all AWS resources
- **Subnet Strategy**: Separate subnets for different security zones
- **Security Groups**: Shared security groups for common access patterns
- **Network ACLs**: Additional network-level security controls

**Security Zones**:
- **Public Zone**: Load balancers and NAT gateways
- **Application Zone**: Application services and APIs
- **Data Zone**: Databases and sensitive data storage
- **Management Zone**: Administrative and monitoring services

### Encryption and Key Management (AWS KMS)
**Purpose**: Centralized encryption key management
**Key Management Strategy**:
- **Master Keys**: Customer-managed keys for different data types
- **Data Encryption**: Automatic encryption for all data at rest
- **Key Rotation**: Automated key rotation policies
- **Access Control**: Fine-grained access control for encryption keys

**Key Hierarchy**:
```
AI-SOC-Platform-Keys/
├── Database-Encryption-Key
├── Cache-Encryption-Key
├── Queue-Encryption-Key
├── Storage-Encryption-Key
└── Application-Encryption-Key
```

## Cost Optimization Shared Infrastructure

### Resource Tagging Strategy
**Purpose**: Cost allocation and resource management across units
**Tagging Schema**:
```
Tags:
  Project: AI-SOC-Platform
  Environment: Production|Staging|Development
  Unit: Infrastructure|Core|AI-Crew|Frontend|Validation
  CostCenter: Security-Operations
  Owner: Platform-Team
  Backup: Required|Optional
```

### Shared Cost Optimization
- **Reserved Instances**: Shared reserved capacity for predictable workloads
- **Spot Instances**: Shared spot instance usage for non-critical workloads
- **Auto-Scaling**: Coordinated scaling across units to optimize costs
- **Resource Scheduling**: Automated resource scheduling for development environments

## Disaster Recovery Shared Infrastructure

### Cross-Region Backup Strategy
**Purpose**: Coordinated disaster recovery across all units
**Backup Components**:
- **Database Replication**: Cross-region replication for all shared databases
- **Configuration Backup**: Parameter Store and Secrets Manager replication
- **Code Repository**: Multi-region Git repository mirrors
- **Infrastructure Code**: Terraform state and configuration backup

### Recovery Coordination
**Recovery Procedures**:
- **Coordinated Failover**: Synchronized failover across all units
- **Data Consistency**: Ensuring data consistency during recovery
- **Service Dependencies**: Managing service startup order during recovery
- **Testing**: Regular disaster recovery testing across all units

This shared infrastructure provides a unified foundation that enables efficient resource utilization, consistent security policies, and coordinated operations across all units of the AI-powered security operations platform.