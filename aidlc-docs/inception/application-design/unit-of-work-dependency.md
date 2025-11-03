# Unit of Work Dependencies

## Dependency Matrix

| Unit | Depends On | Provides Services To | Dependency Type |
|------|------------|---------------------|-----------------|
| Infrastructure & Integration | External AWS Services | All Other Units | Foundation |
| Core Platform Service | Infrastructure & Integration | Frontend Dashboard, Backend Validation | Core Service |
| Network Security AI Crew | Infrastructure & Integration | Core Platform Service | Specialized Service |
| Endpoint Security AI Crew | Infrastructure & Integration | Core Platform Service | Specialized Service |
| Cloud Security AI Crew | Infrastructure & Integration | Core Platform Service | Specialized Service |
| Threat Intelligence AI Crew | Infrastructure & Integration | Core Platform Service | Specialized Service |
| Backend Validation & Explanation | Infrastructure & Integration, Core Platform Service | Frontend Dashboard | Backend Service |
| Frontend Dashboard | Backend Validation & Explanation | End Users (Analysts) | Frontend Service |

## Detailed Dependency Analysis

### Infrastructure & Integration Unit
**Dependencies**: 
- External AWS Bedrock API
- External database systems
- MITRE ATT&CK framework data

**Provides To All Units**:
- Data storage and retrieval services
- AWS Bedrock Claude AI integration
- MITRE framework mapping capabilities
- Configuration management
- Audit logging services
- Health monitoring

**Critical Path**: Must be completed first as foundation for all other units

### Core Platform Service Unit
**Dependencies**:
- Infrastructure & Integration (data storage, AWS integration, MITRE mapping)

**Provides To**:
- Frontend Dashboard (alert data, investigation status)
- Backend Validation & Explanation (investigation findings, AI results)
- All AI Crew Units (coordination and orchestration)

**Integration Points**:
- Receives processed alerts from alert ingestion
- Coordinates with AI crews for specialized analysis
- Sends findings to validation workflows

### AI Crew Units (Network, Endpoint, Cloud, Threat Intelligence)
**Dependencies**:
- Infrastructure & Integration (AWS Bedrock access, data storage)

**Provides To**:
- Core Platform Service (specialized analysis results)

**Integration Pattern**:
- Receive analysis requests from Core Platform Service
- Access AWS Bedrock for AI processing
- Return domain-specific findings and recommendations
- Operate independently but coordinate through Core Platform

### Backend Validation & Explanation Unit
**Dependencies**:
- Infrastructure & Integration (data storage, audit logging)
- Core Platform Service (investigation findings, AI results)

**Provides To**:
- Frontend Dashboard (validation workflows, explanations)

**Integration Points**:
- Receives AI findings from Core Platform Service
- Processes analyst feedback and validation decisions
- Generates plain-English explanations
- Maintains audit trails of human interventions

### Frontend Dashboard Unit
**Dependencies**:
- Backend Validation & Explanation (validation workflows, explanations)

**Provides To**:
- End Users (SOC Analysts)

**Integration Points**:
- Displays real-time alert and investigation data
- Enables analyst interaction with AI findings
- Supports human-in-the-loop validation workflows

## Development Sequence

### Phase 1: Foundation (Week 1-2)
1. **Infrastructure & Integration Unit**
   - Set up data storage (document + relational)
   - Implement AWS Bedrock integration
   - Configure MITRE framework data
   - Establish audit logging and configuration management

### Phase 2: Parallel Development (Week 3-6)
**Track 1: Core Processing**
2. **Core Platform Service Unit**
   - Alert ingestion and triage
   - Investigation orchestration
   - AI crew coordination

**Track 2: AI Specialization**
3. **Network Security AI Crew Unit**
4. **Endpoint Security AI Crew Unit**
5. **Cloud Security AI Crew Unit**
6. **Threat Intelligence AI Crew Unit**

**Track 3: Human Interface**
7. **Backend Validation & Explanation Unit**
   - Validation workflows
   - Explanation generation
   - Analyst notification services

### Phase 3: Integration (Week 7-8)
8. **Frontend Dashboard Unit**
   - Web interface development
   - Real-time data integration
   - Multi-analyst session support

## Inter-Unit Communication Patterns

### Synchronous Communication
- **Frontend Dashboard ↔ Backend Validation**: Real-time user interactions
- **Core Platform ↔ AI Crews**: Critical alert analysis
- **Backend Validation ↔ Infrastructure**: Audit logging

### Asynchronous Communication
- **Core Platform → AI Crews**: Background investigation processing
- **AI Crews → Core Platform**: Analysis result delivery
- **All Units → Infrastructure**: Non-critical data storage and logging

### Event-Driven Communication
- **Core Platform → Backend Validation**: Investigation completion events
- **Backend Validation → Frontend Dashboard**: Validation status updates
- **Infrastructure → All Units**: Configuration change notifications

## Risk Mitigation

### Dependency Risks
1. **Infrastructure Delays**: Could block all other development
   - Mitigation: Prioritize Infrastructure unit, use mocking for early development

2. **AI Crew Integration Complexity**: Multiple crews coordinating through Core Platform
   - Mitigation: Standardized AI crew interface, incremental crew integration

3. **Real-time Frontend Requirements**: Complex real-time data synchronization
   - Mitigation: WebSocket implementation, progressive enhancement approach

### Integration Risks
1. **Cross-Unit Data Consistency**: Multiple units accessing shared data
   - Mitigation: Centralized data management through Infrastructure unit

2. **Performance Bottlenecks**: AI processing and real-time requirements
   - Mitigation: Asynchronous processing, caching strategies, load balancing

3. **Security Boundaries**: Sensitive security data across multiple units
   - Mitigation: Centralized authentication, encrypted inter-unit communication