# Component Methods

## AlertIngestionComponent Methods

### ingestAlert(alertData: AlertData) -> AlertResponse
**Purpose**: Accept and process incoming security alerts
**Input**: AlertData object containing alert details
**Output**: AlertResponse with processing status and alert ID

### normalizeAlert(rawAlert: RawAlert) -> NormalizedAlert
**Purpose**: Convert alerts to standard format
**Input**: RawAlert in various source formats
**Output**: NormalizedAlert in standardized schema

### validateAlert(alert: Alert) -> ValidationResult
**Purpose**: Validate alert data integrity and completeness
**Input**: Alert object to validate
**Output**: ValidationResult with validation status and errors

## AlertTriageComponent Methods

### triageAlert(alert: Alert) -> TriageResult
**Purpose**: Analyze alert and assign risk score and priority
**Input**: Alert object for analysis
**Output**: TriageResult with risk score and priority level

### calculateRiskScore(alert: Alert, context: ThreatContext) -> RiskScore
**Purpose**: Calculate numerical risk score for alert
**Input**: Alert and threat context data
**Output**: RiskScore with numerical value and confidence level

### assignPriority(riskScore: RiskScore) -> Priority
**Purpose**: Convert risk score to priority level
**Input**: RiskScore from analysis
**Output**: Priority enum (Critical, High, Medium, Low)

## InvestigationEngineComponent Methods

### startInvestigation(alert: Alert) -> Investigation
**Purpose**: Initiate automated investigation workflow
**Input**: Alert triggering investigation
**Output**: Investigation object with initial findings

### correlateEvidence(investigation: Investigation) -> CorrelationResult
**Purpose**: Correlate alert with historical data and evidence
**Input**: Investigation context
**Output**: CorrelationResult with related events and patterns

### generateTimeline(investigation: Investigation) -> Timeline
**Purpose**: Create chronological timeline of attack events
**Input**: Investigation with correlated evidence
**Output**: Timeline with ordered sequence of events

### mapToMITRE(findings: InvestigationFindings) -> MITREMapping
**Purpose**: Map investigation findings to MITRE ATT&CK framework
**Input**: InvestigationFindings from analysis
**Output**: MITREMapping with tactics and techniques

## AI Crew Component Methods (Shared Interface)

### analyzeAlert(alert: Alert, domain: SecurityDomain) -> DomainAnalysis
**Purpose**: Perform domain-specific analysis of security alert
**Input**: Alert and security domain context
**Output**: DomainAnalysis with domain-specific findings

### detectThreats(data: SecurityData, domain: SecurityDomain) -> ThreatDetection
**Purpose**: Identify threats specific to security domain
**Input**: SecurityData and domain context
**Output**: ThreatDetection with identified threats

### generateRecommendations(analysis: DomainAnalysis) -> Recommendations
**Purpose**: Generate domain-specific response recommendations
**Input**: DomainAnalysis results
**Output**: Recommendations for threat response

## AnalystDashboardComponent Methods

### getDashboardData(analystId: String) -> DashboardData
**Purpose**: Retrieve real-time dashboard data for analyst
**Input**: Analyst identifier
**Output**: DashboardData with alerts, investigations, and metrics

### updateAlertStatus(alertId: String, status: AlertStatus) -> UpdateResult
**Purpose**: Update alert status based on analyst action
**Input**: Alert ID and new status
**Output**: UpdateResult with success/failure status

### getInvestigationDetails(investigationId: String) -> InvestigationDetails
**Purpose**: Retrieve detailed investigation information
**Input**: Investigation identifier
**Output**: InvestigationDetails with complete investigation data

## ValidationWorkflowComponent Methods

### presentForValidation(findings: AIFindings) -> ValidationRequest
**Purpose**: Present AI findings to analyst for validation
**Input**: AIFindings requiring human review
**Output**: ValidationRequest for analyst interaction

### captureAnalystFeedback(validationId: String, feedback: AnalystFeedback) -> FeedbackResult
**Purpose**: Record analyst validation decisions and feedback
**Input**: Validation ID and analyst feedback
**Output**: FeedbackResult with recorded feedback status

### enableIntervention(investigationId: String) -> InterventionCapability
**Purpose**: Allow analyst to intervene in ongoing investigation
**Input**: Investigation identifier
**Output**: InterventionCapability with available actions

## ExplanationEngineComponent Methods

### generateExplanation(findings: SecurityFindings, analystLevel: ExperienceLevel) -> Explanation
**Purpose**: Create plain-English explanation of security findings
**Input**: SecurityFindings and analyst experience level
**Output**: Explanation tailored to analyst understanding

### provideRecommendations(threat: ThreatAnalysis) -> ActionRecommendations
**Purpose**: Generate context-aware response recommendations
**Input**: ThreatAnalysis results
**Output**: ActionRecommendations with suggested actions

### getLearningResources(threat: ThreatType) -> LearningResources
**Purpose**: Provide educational resources for threat type
**Input**: ThreatType identifier
**Output**: LearningResources with relevant materials

## AWSBedrockIntegrationComponent Methods

### invokeClaudeModel(prompt: String, parameters: ModelParameters) -> ModelResponse
**Purpose**: Send request to AWS Bedrock Claude model
**Input**: Prompt text and model parameters
**Output**: ModelResponse with AI-generated content

### authenticateAWS() -> AuthenticationResult
**Purpose**: Authenticate with AWS Bedrock service
**Input**: None (uses configured credentials)
**Output**: AuthenticationResult with authentication status

### handleAPIError(error: AWSError) -> ErrorResponse
**Purpose**: Process and handle AWS API errors
**Input**: AWSError from failed request
**Output**: ErrorResponse with error handling result

## MITREAttackMappingComponent Methods

### mapFindingsToFramework(findings: SecurityFindings) -> MITREMapping
**Purpose**: Map security findings to MITRE ATT&CK tactics and techniques
**Input**: SecurityFindings from investigation
**Output**: MITREMapping with framework associations

### getFrameworkData() -> MITREFrameworkData
**Purpose**: Retrieve current MITRE ATT&CK framework data
**Input**: None
**Output**: MITREFrameworkData with tactics and techniques

### generateAttackChain(mappings: List<MITREMapping>) -> AttackChain
**Purpose**: Create attack chain visualization from MITRE mappings
**Input**: List of MITRE mappings
**Output**: AttackChain with visualized attack progression

## DataStorageComponent Methods

### storeInvestigationData(investigation: Investigation) -> StorageResult
**Purpose**: Store flexible investigation data in document storage
**Input**: Investigation object with variable structure
**Output**: StorageResult with storage confirmation

### storeStructuredData(data: StructuredData, table: String) -> StorageResult
**Purpose**: Store structured data in relational format
**Input**: StructuredData and target table name
**Output**: StorageResult with storage confirmation

### queryInvestigations(criteria: QueryCriteria) -> QueryResult
**Purpose**: Query investigation data with flexible criteria
**Input**: QueryCriteria for search parameters
**Output**: QueryResult with matching investigations