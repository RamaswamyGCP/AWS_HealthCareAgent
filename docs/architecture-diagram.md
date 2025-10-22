# 🏥 Hospital Multi-Agent System Architecture

## High-Level System Architecture

```mermaid
graph TB
    subgraph "Frontend Layer"
        UI[🎨 Streamlit UI]
        API[🌐 REST API]
        MOBILE[📱 Mobile App]
    end
    
    subgraph "API Gateway Layer"
        GATEWAY[⚡ AWS API Gateway]
        AUTH[🔐 Authentication]
        RATE[📊 Rate Limiting]
    end
    
    subgraph "Agent Orchestration Layer"
        SUPERVISOR[🤖 Supervisor Agent<br/>Route & Coordinate]
        MEMORY[🧠 Memory Manager<br/>Session & Long-term]
    end
    
    subgraph "Specialized Agents"
        TRIAGE[🩺 Triage Agent<br/>Symptom Analysis]
        BOOKING[📅 Booking Agent<br/>Appointments]
        REMINDER[⏰ Reminder Agent<br/>Notifications]
        PHARMACY[💊 Pharmacy Agent<br/>Prescriptions]
    end
    
    subgraph "Tool Functions (Lambda)"
        TOOLS1[🔍 Search Symptoms]
        TOOLS2[📋 Patient History]
        TOOLS3[📅 Check Availability]
        TOOLS4[📧 Send Notifications]
        TOOLS5[💊 Prescription Tools]
    end
    
    subgraph "Data Layer"
        PATIENTS[(👥 Patients Table<br/>DynamoDB)]
        APPOINTMENTS[(📅 Appointments<br/>DynamoDB)]
        MEMORY_DB[(🧠 Memory Store<br/>DynamoDB)]
        PRESCRIPTIONS[(💊 Prescriptions<br/>DynamoDB)]
    end
    
    subgraph "External Services"
        BEDROCK[🤖 AWS Bedrock<br/>Claude 3.5 Sonnet]
        SNS[📱 AWS SNS<br/>Notifications]
        SES[📧 AWS SES<br/>Email]
    end
    
    %% Connections
    UI --> GATEWAY
    API --> GATEWAY
    MOBILE --> GATEWAY
    
    GATEWAY --> AUTH
    GATEWAY --> RATE
    GATEWAY --> SUPERVISOR
    
    SUPERVISOR --> MEMORY
    SUPERVISOR --> TRIAGE
    SUPERVISOR --> BOOKING
    SUPERVISOR --> REMINDER
    SUPERVISOR --> PHARMACY
    
    TRIAGE --> TOOLS1
    TRIAGE --> TOOLS2
    BOOKING --> TOOLS3
    REMINDER --> TOOLS4
    PHARMACY --> TOOLS5
    
    TOOLS1 --> PATIENTS
    TOOLS2 --> PATIENTS
    TOOLS2 --> MEMORY_DB
    TOOLS3 --> APPOINTMENTS
    TOOLS4 --> SNS
    TOOLS4 --> SES
    TOOLS5 --> PRESCRIPTIONS
    
    SUPERVISOR --> BEDROCK
    TRIAGE --> BEDROCK
    BOOKING --> BEDROCK
    REMINDER --> BEDROCK
    PHARMACY --> BEDROCK
    
    MEMORY --> MEMORY_DB
    
    classDef frontend fill:#e1f5fe
    classDef agents fill:#f3e5f5
    classDef tools fill:#fff3e0
    classDef data fill:#e8f5e8
    classDef external fill:#fce4ec
    
    class UI,API,MOBILE frontend
    class SUPERVISOR,TRIAGE,BOOKING,REMINDER,PHARMACY agents
    class TOOLS1,TOOLS2,TOOLS3,TOOLS4,TOOLS5 tools
    class PATIENTS,APPOINTMENTS,MEMORY_DB,PRESCRIPTIONS data
    class BEDROCK,SNS,SES external
```

## Agent Communication Flow

```mermaid
sequenceDiagram
    participant User
    participant UI as Streamlit UI
    participant Supervisor as Supervisor Agent
    participant Triage as Triage Agent
    participant Memory as Memory Store
    participant Tools as Lambda Tools
    participant DB as DynamoDB
    participant Bedrock as AWS Bedrock

    User->>UI: "My child has fever and cough"
    UI->>Supervisor: Route query with patient_id
    
    Supervisor->>Memory: Check patient history
    Memory->>DB: Query patient data
    DB-->>Memory: Patient profile + medical history
    Memory-->>Supervisor: Patient context
    
    Supervisor->>Bedrock: Analyze query intent
    Bedrock-->>Supervisor: Route to Triage Agent
    
    Supervisor->>Triage: Forward query + context
    Triage->>Tools: Search symptoms
    Tools->>DB: Query symptom database
    DB-->>Tools: Symptom analysis
    Tools-->>Triage: Symptom results
    
    Triage->>Bedrock: Generate triage response
    Bedrock-->>Triage: Triage recommendation
    
    Triage->>Memory: Store interaction
    Memory->>DB: Save session data
    
    Triage-->>Supervisor: Triage response
    Supervisor-->>UI: Final response
    UI-->>User: "High urgency - go to ER"
```

## Data Flow Architecture

```mermaid
graph LR
    subgraph "Input Processing"
        INPUT[User Query]
        PARSE[Query Parser]
        CONTEXT[Context Builder]
    end
    
    subgraph "Agent Processing"
        ROUTE[Route Decision]
        AGENT[Specialized Agent]
        TOOLS[Tool Execution]
    end
    
    subgraph "Data Operations"
        READ[Read Patient Data]
        PROCESS[Process Information]
        WRITE[Write Results]
    end
    
    subgraph "Response Generation"
        GENERATE[Generate Response]
        FORMAT[Format Output]
        DELIVER[Deliver to User]
    end
    
    INPUT --> PARSE
    PARSE --> CONTEXT
    CONTEXT --> ROUTE
    ROUTE --> AGENT
    AGENT --> TOOLS
    TOOLS --> READ
    READ --> PROCESS
    PROCESS --> WRITE
    WRITE --> GENERATE
    GENERATE --> FORMAT
    FORMAT --> DELIVER
    
    classDef input fill:#e3f2fd
    classDef processing fill:#f1f8e9
    classDef data fill:#fff8e1
    classDef output fill:#fce4ec
    
    class INPUT,PARSE,CONTEXT input
    class ROUTE,AGENT,TOOLS processing
    class READ,PROCESS,WRITE data
    class GENERATE,FORMAT,DELIVER output
```

## AWS Services Integration

```mermaid
graph TB
    subgraph "Compute Services"
        LAMBDA[AWS Lambda<br/>Tool Functions]
        BEDROCK[AWS Bedrock<br/>AgentCore Runtime]
    end
    
    subgraph "Storage Services"
        DYNAMO[DynamoDB<br/>Patient Data]
        S3[S3 Bucket<br/>Documents & Logs]
    end
    
    subgraph "Integration Services"
        GATEWAY[API Gateway<br/>REST Endpoints]
        SNS[SNS<br/>Push Notifications]
        SES[SES<br/>Email Service]
    end
    
    subgraph "Security & Monitoring"
        IAM[IAM Roles<br/>Access Control]
        CLOUDWATCH[CloudWatch<br/>Monitoring & Logs]
        XRAY[X-Ray<br/>Distributed Tracing]
    end
    
    BEDROCK --> LAMBDA
    LAMBDA --> DYNAMO
    LAMBDA --> S3
    LAMBDA --> SNS
    LAMBDA --> SES
    
    GATEWAY --> BEDROCK
    
    IAM --> BEDROCK
    IAM --> LAMBDA
    IAM --> DYNAMO
    
    CLOUDWATCH --> BEDROCK
    CLOUDWATCH --> LAMBDA
    XRAY --> BEDROCK
    
    classDef compute fill:#ff9800
    classDef storage fill:#4caf50
    classDef integration fill:#2196f3
    classDef security fill:#9c27b0
    
    class LAMBDA,BEDROCK compute
    class DYNAMO,S3 storage
    class GATEWAY,SNS,SES integration
    class IAM,CLOUDWATCH,XRAY security
```

## Security Architecture

```mermaid
graph TB
    subgraph "Authentication Layer"
        COGNITO[AWS Cognito<br/>User Authentication]
        JWT[JWT Tokens<br/>Session Management]
    end
    
    subgraph "Authorization Layer"
        IAM[IAM Policies<br/>Service Access]
        RBAC[Role-Based Access<br/>Patient Data]
    end
    
    subgraph "Data Protection"
        ENCRYPT[Encryption at Rest<br/>DynamoDB KMS]
        TLS[TLS 1.3<br/>Data in Transit]
        HIPAA[HIPAA Compliance<br/>PHI Protection]
    end
    
    subgraph "Monitoring & Audit"
        CLOUDTRAIL[CloudTrail<br/>API Audit Logs]
        GUARDDUTY[GuardDuty<br/>Threat Detection]
        CONFIG[Config Rules<br/>Compliance Monitoring]
    end
    
    COGNITO --> JWT
    JWT --> IAM
    IAM --> RBAC
    
    RBAC --> ENCRYPT
    ENCRYPT --> TLS
    TLS --> HIPAA
    
    HIPAA --> CLOUDTRAIL
    CLOUDTRAIL --> GUARDDUTY
    GUARDDUTY --> CONFIG
    
    classDef auth fill:#4caf50
    classDef authz fill:#ff9800
    classDef protection fill:#f44336
    classDef monitoring fill:#9c27b0
    
    class COGNITO,JWT auth
    class IAM,RBAC authz
    class ENCRYPT,TLS,HIPAA protection
    class CLOUDTRAIL,GUARDDUTY,CONFIG monitoring
```

## Deployment Architecture

```mermaid
graph TB
    subgraph "Development Environment"
        DEV_CODE[Local Development]
        DEV_TEST[Unit Testing]
        DEV_LINT[Code Quality]
    end
    
    subgraph "CI/CD Pipeline"
        GITHUB[GitHub Repository]
        ACTIONS[GitHub Actions]
        BUILD[Build & Package]
        TEST[Integration Tests]
    end
    
    subgraph "Staging Environment"
        STAGE_DEPLOY[SAM Deploy Staging]
        STAGE_TEST[End-to-End Tests]
        STAGE_VALIDATE[Performance Tests]
    end
    
    subgraph "Production Environment"
        PROD_DEPLOY[SAM Deploy Production]
        PROD_MONITOR[CloudWatch Monitoring]
        PROD_ALERT[Alert Management]
    end
    
    DEV_CODE --> GITHUB
    DEV_TEST --> GITHUB
    DEV_LINT --> GITHUB
    
    GITHUB --> ACTIONS
    ACTIONS --> BUILD
    BUILD --> TEST
    
    TEST --> STAGE_DEPLOY
    STAGE_DEPLOY --> STAGE_TEST
    STAGE_TEST --> STAGE_VALIDATE
    
    STAGE_VALIDATE --> PROD_DEPLOY
    PROD_DEPLOY --> PROD_MONITOR
    PROD_MONITOR --> PROD_ALERT
    
    classDef dev fill:#e8f5e8
    classDef cicd fill:#fff3e0
    classDef staging fill:#e1f5fe
    classDef prod fill:#fce4ec
    
    class DEV_CODE,DEV_TEST,DEV_LINT dev
    class GITHUB,ACTIONS,BUILD,TEST cicd
    class STAGE_DEPLOY,STAGE_TEST,STAGE_VALIDATE staging
    class PROD_DEPLOY,PROD_MONITOR,PROD_ALERT prod
```

## Cost Optimization Architecture

```mermaid
graph LR
    subgraph "Cost Drivers"
        BEDROCK_COST[Bedrock API Calls<br/>~$0.003/1K tokens]
        LAMBDA_COST[Lambda Invocations<br/>~$0.20/1M requests]
        DYNAMO_COST[DynamoDB Operations<br/>~$1.25/million RCU]
        GATEWAY_COST[API Gateway<br/>~$3.50/million calls]
    end
    
    subgraph "Optimization Strategies"
        CACHE[Response Caching<br/>Reduce Bedrock calls]
        BATCH[Batch Processing<br/>Optimize Lambda]
        ONDEMAND[On-Demand Billing<br/>DynamoDB scaling]
        COMPRESS[Response Compression<br/>Reduce bandwidth]
    end
    
    BEDROCK_COST --> CACHE
    LAMBDA_COST --> BATCH
    DYNAMO_COST --> ONDEMAND
    GATEWAY_COST --> COMPRESS
    
    classDef cost fill:#f44336
    classDef optimization fill:#4caf50
    
    class BEDROCK_COST,LAMBDA_COST,DYNAMO_COST,GATEWAY_COST cost
    class CACHE,BATCH,ONDEMAND,COMPRESS optimization
```

## Next Steps for Architecture Enhancement

1. **Add Real-time Features**: WebSocket support for live chat
2. **Implement Caching**: Redis for frequently accessed patient data
3. **Add Analytics**: Real-time dashboards for hospital operations
4. **Enhance Security**: Advanced threat detection and response
5. **Scale Globally**: Multi-region deployment for disaster recovery
6. **Add ML Pipeline**: Custom models for specialized medical tasks
