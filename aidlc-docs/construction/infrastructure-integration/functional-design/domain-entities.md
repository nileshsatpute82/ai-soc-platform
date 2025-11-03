# Infrastructure & Integration - Domain Entities

## Core Domain Entities

### DataStorageEntity
**Purpose**: Represents data items in the hybrid storage system

**Attributes**:
- `id`: Unique identifier (UUID)
- `dataType`: Classification (STRUCTURED, FLEXIBLE)
- `storageLocation`: Storage system (RELATIONAL, DOCUMENT)
- `schema`: Data structure definition
- `metadata`: Additional data properties
- `createdAt`: Creation timestamp
- `updatedAt`: Last modification timestamp
- `version`: Data version for consistency

**Relationships**:
- Has many `AuditEvent` (audit trail)
- References `StorageConfiguration` (storage rules)

### AWSBedrockRequest
**Purpose**: Represents AI processing requests to AWS Bedrock

**Attributes**:
- `requestId`: Unique request identifier
- `prompt`: AI prompt text
- `parameters`: Model parameters (temperature, max_tokens)
- `batchId`: Batch identifier for grouped requests
- `priority`: Request priority (HIGH, NORMAL, LOW)
- `status`: Processing status (PENDING, PROCESSING, COMPLETED, FAILED)
- `cacheKey`: Cache lookup key
- `submittedAt`: Request submission time
- `completedAt`: Request completion time
- `retryCount`: Number of retry attempts

**Relationships**:
- Belongs to `AWSBedrockBatch` (batching)
- Has one `AWSBedrockResponse` (response)
- Has many `AuditEvent` (audit trail)

### AWSBedrockResponse
**Purpose**: Represents AI processing responses from AWS Bedrock

**Attributes**:
- `responseId`: Unique response identifier
- `requestId`: Associated request identifier
- `content`: AI-generated content
- `confidence`: Response confidence score
- `tokenUsage`: Token consumption metrics
- `processingTime`: Response generation time
- `cacheExpiry`: Cache expiration timestamp
- `errorCode`: Error code if failed
- `errorMessage`: Error description if failed

**Relationships**:
- Belongs to `AWSBedrockRequest` (request-response)
- Has many `AuditEvent` (audit trail)

### MITREFrameworkVersion
**Purpose**: Represents MITRE ATT&CK framework versions

**Attributes**:
- `versionId`: Framework version identifier
- `versionNumber`: Semantic version (e.g., "12.1")
- `releaseDate`: Framework release date
- `status`: Version status (ACTIVE, DEPRECATED, ROLLBACK)
- `changesSummary`: Summary of changes from previous version
- `riskLevel`: Update risk assessment (LOW, MEDIUM, HIGH)
- `approvalStatus`: Approval workflow status
- `installedAt`: Installation timestamp
- `rollbackAvailable`: Rollback capability flag

**Relationships**:
- Has many `MITRETechnique` (techniques)
- Has many `MITRETactic` (tactics)
- Has many `FrameworkChangeLog` (change history)

### MITRETechnique
**Purpose**: Represents individual MITRE ATT&CK techniques

**Attributes**:
- `techniqueId`: MITRE technique ID (e.g., "T1055")
- `name`: Technique name
- `description`: Technique description
- `tactics`: Associated tactics list
- `platforms`: Applicable platforms
- `dataSource`: Detection data sources
- `versionId`: Framework version reference
- `isNew`: New technique flag
- `isModified`: Modified technique flag
- `isDeprecated`: Deprecated technique flag

**Relationships**:
- Belongs to `MITREFrameworkVersion` (version)
- Has many `ThreatMapping` (threat mappings)

### AuditEvent
**Purpose**: Represents system audit events with tiered classification

**Attributes**:
- `eventId`: Unique event identifier
- `eventType`: Type of event (USER_ACTION, SYSTEM_OPERATION, SECURITY_EVENT)
- `tier`: Audit tier (CRITICAL, HIGH, MEDIUM, LOW)
- `userId`: User identifier (if applicable)
- `component`: Source component name
- `action`: Action performed
- `resource`: Affected resource
- `result`: Operation result (SUCCESS, FAILURE, PARTIAL)
- `details`: Additional event details
- `timestamp`: Event occurrence time
- `retentionExpiry`: Retention expiration date
- `accessLevel`: Required access level to view

**Relationships**:
- References `User` (user actions)
- References various entities (polymorphic)

### ConfigurationItem
**Purpose**: Represents system configuration items

**Attributes**:
- `configId`: Configuration item identifier
- `key`: Configuration key
- `value`: Configuration value
- `environment`: Target environment (DEV, STAGING, PROD)
- `component`: Owning component
- `dataType`: Value data type
- `isSecret`: Secret configuration flag
- `version`: Configuration version
- `status`: Configuration status (ACTIVE, PENDING, DEPRECATED)
- `validationRules`: Validation rule set
- `dependencies`: Configuration dependencies
- `createdBy`: Creator user ID
- `approvedBy`: Approver user ID
- `deployedAt`: Deployment timestamp

**Relationships**:
- Has many `ConfigurationChange` (change history)
- Has many `ValidationResult` (validation results)

### SystemHealthMetric
**Purpose**: Represents system health and performance metrics

**Attributes**:
- `metricId`: Unique metric identifier
- `component`: Source component name
- `metricName`: Metric name (CPU_USAGE, MEMORY_USAGE, RESPONSE_TIME)
- `value`: Metric value
- `unit`: Measurement unit
- `threshold`: Alert threshold
- `status`: Health status (HEALTHY, WARNING, CRITICAL)
- `timestamp`: Measurement timestamp
- `tags`: Additional metric tags

**Relationships**:
- Has many `HealthAlert` (generated alerts)

## Supporting Domain Entities

### StorageConfiguration
**Purpose**: Configuration for data storage routing rules

**Attributes**:
- `ruleId`: Storage rule identifier
- `dataTypePattern`: Data type matching pattern
- `storageType`: Target storage type
- `priority`: Rule priority
- `isActive`: Rule active status

### CircuitBreakerState
**Purpose**: Circuit breaker state for AWS Bedrock integration

**Attributes**:
- `serviceId`: Service identifier
- `state`: Circuit state (CLOSED, OPEN, HALF_OPEN)
- `failureCount`: Consecutive failure count
- `lastFailureTime`: Last failure timestamp
- `nextRetryTime`: Next retry attempt time

### CacheEntry
**Purpose**: Cache entries for AWS Bedrock responses

**Attributes**:
- `cacheKey`: Cache lookup key
- `content`: Cached content
- `expiryTime`: Cache expiration time
- `hitCount`: Cache hit counter
- `createdAt`: Cache creation time

### ValidationResult
**Purpose**: Configuration validation results

**Attributes**:
- `validationId`: Validation identifier
- `configId`: Configuration item reference
- `isValid`: Validation result
- `errorMessages`: Validation error messages
- `validatedAt`: Validation timestamp

### HealthAlert
**Purpose**: System health alerts

**Attributes**:
- `alertId`: Alert identifier
- `metricId`: Source metric reference
- `severity`: Alert severity
- `message`: Alert message
- `isResolved`: Resolution status
- `createdAt`: Alert creation time
- `resolvedAt`: Alert resolution time

## Entity Relationships Summary

### Primary Relationships
- **DataStorageEntity** ↔ **AuditEvent**: All data operations generate audit events
- **AWSBedrockRequest** ↔ **AWSBedrockResponse**: Request-response pairs
- **MITREFrameworkVersion** ↔ **MITRETechnique**: Version contains techniques
- **ConfigurationItem** ↔ **ValidationResult**: Configuration validation results
- **SystemHealthMetric** ↔ **HealthAlert**: Metrics generate alerts

### Cross-Entity Relationships
- All entities can have associated **AuditEvent** records
- **ConfigurationItem** affects behavior of all other entities
- **SystemHealthMetric** monitors performance of all components
- **MITRETechnique** referenced by threat analysis entities (other units)

## Data Consistency Rules

### Entity Lifecycle
1. **Creation**: All entities must have valid creation timestamps and audit events
2. **Modification**: Updates must increment version numbers and generate audit events
3. **Deletion**: Soft deletion preferred with audit trail maintenance
4. **Archival**: Expired entities moved to archival storage per retention policies

### Referential Integrity
- Foreign key relationships must be maintained across storage types
- Orphaned references cleaned up through automated processes
- Cross-storage references use eventual consistency model
- Cascade operations limited to prevent data loss