# Units of Work

## System Decomposition Overview
**Architecture**: Hybrid approach with core platform service and specialized AI crew services
**Development Strategy**: Parallel development of AI processing and human interface units

## Unit Definitions

### Unit 1: Core Platform Service
**Purpose**: Central alert processing, triage, and investigation orchestration
**Type**: Core Service
**Development Priority**: High (Parallel Track 1)

**Components**:
- AlertIngestionComponent
- AlertTriageComponent  
- InvestigationEngineComponent
- AlertProcessingService
- InvestigationService
- AICrewCoordinationService

**Responsibilities**:
- Accept and normalize security alerts from multiple sources
- Perform automated risk assessment and prioritization
- Orchestrate investigation workflows across AI crews
- Coordinate multi-domain AI analysis
- Manage alert lifecycle from ingestion to resolution
- Implement hybrid priority-based routing (sync/async)

**Key Features**:
- Real-time alert processing (30-second target)
- Risk-based priority assignment
- Investigation timeline generation
- Cross-crew coordination and consensus building

### Unit 2: Network Security AI Crew
**Purpose**: Specialized AI analysis for network-based security threats
**Type**: AI Crew Service
**Development Priority**: High (Parallel Track 2)

**Components**:
- NetworkSecurityCrewComponent

**Responsibilities**:
- Analyze network traffic patterns and anomalies
- Detect network-based attack indicators
- Investigate network infrastructure threats
- Generate network-specific threat recommendations
- Correlate network events with attack patterns

**Key Features**:
- Network behavior analysis
- Traffic pattern recognition
- Network-based IOC detection
- Network topology threat assessment

### Unit 3: Endpoint Security AI Crew
**Purpose**: Specialized AI analysis for endpoint security threats
**Type**: AI Crew Service
**Development Priority**: High (Parallel Track 2)

**Components**:
- EndpointSecurityCrewComponent

**Responsibilities**:
- Analyze endpoint behavior and process anomalies
- Detect malware and suspicious executable patterns
- Investigate host-based indicators of compromise
- Generate endpoint remediation recommendations
- Correlate endpoint events across multiple hosts

**Key Features**:
- Process behavior analysis
- Malware signature detection
- Host-based IOC correlation
- Endpoint remediation guidance

### Unit 4: Cloud Security AI Crew
**Purpose**: Specialized AI analysis for cloud security threats
**Type**: AI Crew Service
**Development Priority**: High (Parallel Track 2)

**Components**:
- CloudSecurityCrewComponent

**Responsibilities**:
- Analyze cloud service configurations and access patterns
- Detect cloud-specific attack vectors and misconfigurations
- Investigate cloud infrastructure threats and compliance issues
- Generate cloud security recommendations and remediation steps
- Monitor cloud resource usage anomalies

**Key Features**:
- Cloud configuration assessment
- Access pattern analysis
- Cloud-native threat detection
- Compliance monitoring

### Unit 5: Threat Intelligence AI Crew
**Purpose**: Specialized AI analysis using threat intelligence data
**Type**: AI Crew Service
**Development Priority**: High (Parallel Track 2)

**Components**:
- ThreatIntelligenceCrewComponent

**Responsibilities**:
- Correlate alerts with external threat intelligence feeds
- Identify known threat actors, campaigns, and TTPs
- Analyze indicators of compromise (IOCs) against threat databases
- Generate threat attribution and context analysis
- Provide threat landscape awareness

**Key Features**:
- Threat intelligence correlation
- Actor attribution analysis
- Campaign pattern recognition
- IOC enrichment and validation

### Unit 6: Frontend Dashboard
**Purpose**: Web-based analyst interface and real-time monitoring
**Type**: Frontend Service
**Development Priority**: High (Parallel Track 1)

**Components**:
- AnalystDashboardComponent

**Responsibilities**:
- Provide dark-themed web interface for SOC operations
- Display real-time alert status and investigation progress
- Enable analyst interaction with AI findings and recommendations
- Support multiple concurrent analyst sessions
- Implement responsive design for various screen sizes

**Key Features**:
- Real-time dashboard updates
- Interactive investigation views
- Multi-analyst session support
- Dark theme UI/UX
- Mobile-responsive design

### Unit 7: Backend Validation & Explanation
**Purpose**: Human-in-the-loop validation and plain-English explanations
**Type**: Backend Service
**Development Priority**: High (Parallel Track 1)

**Components**:
- ValidationWorkflowComponent
- ExplanationEngineComponent
- ValidationService
- ExplanationService
- AnalystNotificationService

**Responsibilities**:
- Implement continuous monitoring with intervention capabilities
- Present AI findings for analyst review and validation
- Generate plain-English threat explanations for junior analysts
- Capture analyst feedback and maintain audit trails
- Provide context-aware recommendations and learning resources

**Key Features**:
- Continuous monitoring workflows
- Real-time intervention capabilities
- Adaptive explanation generation
- Comprehensive audit logging
- Multi-level analyst support

### Unit 8: Infrastructure & Integration
**Purpose**: Data storage, AWS integrations, and MITRE framework support
**Type**: Infrastructure Service
**Development Priority**: Medium (Foundation)

**Components**:
- DataStorageComponent
- AWSBedrockIntegrationComponent
- MITREAttackMappingComponent
- DataManagementService
- AWSIntegrationService
- AuditService
- ConfigurationService
- HealthMonitoringService

**Responsibilities**:
- Manage hybrid data storage (document + relational)
- Handle AWS Bedrock Claude API integrations
- Maintain MITRE ATT&CK framework mappings
- Provide centralized configuration management
- Implement comprehensive audit logging
- Monitor system health and performance

**Key Features**:
- Hybrid storage architecture
- Direct AWS Bedrock integration
- MITRE framework automation
- Centralized configuration
- Health monitoring and alerting

## Unit Characteristics Summary

| Unit | Type | Components | Development Track | Dependencies |
|------|------|------------|------------------|--------------|
| Core Platform Service | Core Service | 6 components | Parallel Track 1 | Infrastructure Unit |
| Network Security AI Crew | AI Crew Service | 1 component | Parallel Track 2 | Infrastructure Unit |
| Endpoint Security AI Crew | AI Crew Service | 1 component | Parallel Track 2 | Infrastructure Unit |
| Cloud Security AI Crew | AI Crew Service | 1 component | Parallel Track 2 | Infrastructure Unit |
| Threat Intelligence AI Crew | AI Crew Service | 1 component | Parallel Track 2 | Infrastructure Unit |
| Frontend Dashboard | Frontend Service | 1 component | Parallel Track 1 | Backend Validation Unit |
| Backend Validation & Explanation | Backend Service | 5 components | Parallel Track 1 | Infrastructure Unit |
| Infrastructure & Integration | Infrastructure Service | 8 components | Foundation | None |

## Development Approach
- **Foundation First**: Infrastructure & Integration unit provides base services
- **Parallel Development**: Core Platform and Frontend/Backend units develop simultaneously
- **AI Crew Integration**: Specialized AI crews integrate with Core Platform as they complete
- **Incremental Delivery**: Each unit can be tested and validated independently