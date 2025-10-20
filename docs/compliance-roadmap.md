# 🔒 Compliance Roadmap: From MVP to HIPAA Production

This document outlines the path from the **hackathon MVP** to a **HIPAA-compliant production system**.

---

## Current State (MVP)

### ✅ What We Have
- AWS-native architecture (inherent security benefits)
- IAM role-based access control
- DynamoDB encryption at rest (default)
- HTTPS endpoints (API Gateway)
- No credentials in code
- CloudWatch logging

### ⚠️ What's Missing for HIPAA
- BAA (Business Associate Agreement) with AWS
- HealthLake for FHIR compliance
- Enhanced encryption (KMS)
- Cognito authentication
- Audit trails (CloudTrail)
- PHI data handling procedures
- Data retention policies
- Disaster recovery plan

---

## Production Roadmap

### Phase 1: Enhanced Security (Week 1-2)

#### 1.1 Enable KMS Encryption
**Current**: DynamoDB default encryption  
**Target**: Customer-managed KMS keys

```yaml
# template.yaml addition
DynamoDBKeyPolicy:
  Type: AWS::KMS::Key
  Properties:
    Description: KMS key for patient data encryption
    KeyPolicy:
      # Key rotation every 365 days
      EnableKeyRotation: true
```

**Effort**: 2 hours  
**Cost**: +$1/month per key

#### 1.2 Add Cognito Authentication
**Current**: No authentication (IAM only)  
**Target**: Cognito User Pools with MFA

```python
# Add to API Gateway
Authorizer:
  Type: COGNITO_USER_POOLS
  ProviderARNs:
    - !GetAtt UserPool.Arn
  AuthorizationScopes:
    - hospital/read
    - hospital/write
```

**Effort**: 4 hours  
**Cost**: $0.0055 per MAU (Monthly Active User)

#### 1.3 Enable CloudTrail
**Current**: Basic CloudWatch logs  
**Target**: Comprehensive audit trails

```yaml
HospitalAuditTrail:
  Type: AWS::CloudTrail::Trail
  Properties:
    IsLogging: true
    IncludeGlobalServiceEvents: true
    EventSelectors:
      - ReadWriteType: All
        IncludeManagementEvents: true
        DataResources:
          - Type: AWS::DynamoDB::Table
            Values: [!GetAtt PatientsTable.Arn]
```

**Effort**: 2 hours  
**Cost**: ~$2/month (first copy free)

---

### Phase 2: HIPAA Compliance (Week 3-4)

#### 2.1 Migrate to HealthLake
**Current**: DynamoDB with FHIR-like schema  
**Target**: AWS HealthLake for true FHIR R4 compliance

```python
# Migration script
from fhir.resources.patient import Patient

def migrate_patient_to_healthlake(dynamodb_patient):
    fhir_patient = Patient(
        id=dynamodb_patient['patient_id'],
        name=[{
            "family": dynamodb_patient['name'].split()[-1],
            "given": dynamodb_patient['name'].split()[:-1]
        }],
        birthDate=dynamodb_patient['date_of_birth'],
        # ... full FHIR mapping
    )
    
    healthlake.create_resource(
        DatastoreId=DATASTORE_ID,
        Resource=fhir_patient.json()
    )
```

**Effort**: 16 hours (schema mapping + migration)  
**Cost**: $1.00 per GB stored/month + data transfer

#### 2.2 Sign AWS BAA
**Current**: Standard AWS terms  
**Target**: HIPAA-compliant BAA

1. Navigate to AWS Artifact
2. Download HIPAA BAA
3. Complete and submit
4. Enable HIPAA-eligible services only

**Effort**: 1 hour (paperwork)  
**Cost**: Free

#### 2.3 Implement RBAC
**Current**: Simple IAM roles  
**Target**: Fine-grained role-based access

```python
# Example policy
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "healthlake:ReadResource",
        "healthlake:SearchWithGet"
      ],
      "Resource": "arn:aws:healthlake:*:*:datastore/*",
      "Condition": {
        "StringEquals": {
          "aws:PrincipalOrgID": "${OrganizationId}"
        }
      }
    }
  ]
}
```

Roles:
- `PhysicianRole`: Read/Write patient data
- `NurseRole`: Read patient data, limited write
- `ReceptionistRole`: Scheduling only
- `PatientRole`: Own data only

**Effort**: 8 hours  
**Cost**: Free (IAM)

---

### Phase 3: Data Governance (Week 5-6)

#### 3.1 Data Retention Policies
**Current**: Indefinite retention  
**Target**: Automated lifecycle management

```python
# DynamoDB TTL for temporary data
AppointmentsTable:
  TimeToLiveSpecification:
    Enabled: true
    AttributeName: expiration_time

# S3 Lifecycle for logs
LogBucket:
  LifecycleConfiguration:
    Rules:
      - Id: DeleteOldLogs
        Status: Enabled
        ExpirationInDays: 90  # HIPAA minimum: 6 years for PHI
```

**Effort**: 4 hours  
**Cost**: Neutral (reduces storage)

#### 3.2 PHI Redaction
**Current**: No PII/PHI protection  
**Target**: Automatic redaction in logs

```python
import boto3

comprehend = boto3.client('comprehendmedical')

def redact_phi(text):
    response = comprehend.detect_phi(Text=text)
    
    for entity in response['Entities']:
        if entity['Category'] in ['NAME', 'ID', 'ADDRESS']:
            text = text.replace(entity['Text'], '[REDACTED]')
    
    return text

# Use in CloudWatch logs
logger.info(redact_phi(f"Patient {patient_name} checked in"))
```

**Effort**: 6 hours  
**Cost**: $0.01 per 100 characters (Comprehend Medical)

#### 3.3 Disaster Recovery
**Current**: Single-region deployment  
**Target**: Multi-region with automated backups

```yaml
# Enable Point-in-Time Recovery
PatientsTable:
  PointInTimeRecoverySpecification:
    PointInTimeRecoveryEnabled: true

# Cross-region replication
PatientsTableReplica:
  Type: AWS::DynamoDB::GlobalTable
  Properties:
    Replicas:
      - Region: us-east-1
      - Region: us-west-2
```

**Effort**: 8 hours  
**Cost**: +50% (replication)

---

### Phase 4: Monitoring & Compliance (Week 7-8)

#### 4.1 Compliance Dashboard
**Current**: Basic metrics  
**Target**: Real-time compliance monitoring

```python
# AWS Config rules
ComplianceRules:
  - encrypted-volumes
  - access-keys-rotated
  - mfa-enabled
  - cloudtrail-enabled
  - s3-bucket-public-read-prohibited
```

**Effort**: 8 hours  
**Cost**: $0.003 per config evaluation

#### 4.2 Penetration Testing
**Current**: None  
**Target**: Quarterly penetration tests

1. Engage AWS-approved vendor
2. Test authentication, authorization, data access
3. Remediate findings
4. Document for compliance

**Effort**: 40 hours (quarterly)  
**Cost**: $5,000-$15,000 per test

#### 4.3 Staff Training
**Current**: Developer knowledge only  
**Target**: HIPAA-trained team

- HIPAA basics training (all staff)
- Technical controls training (dev team)
- Incident response training (ops team)
- Quarterly refreshers

**Effort**: 16 hours (one-time) + 4 hours quarterly  
**Cost**: $1,000-$3,000 (training materials)

---

## Cost Summary

| Phase | One-Time | Monthly Recurring |
|-------|----------|-------------------|
| **MVP (Current)** | $0 | ~$8 |
| **Phase 1: Enhanced Security** | $0 | +$10 |
| **Phase 2: HIPAA Compliance** | $5,000 | +$50 |
| **Phase 3: Data Governance** | $2,000 | +$20 |
| **Phase 4: Monitoring** | $10,000 | +$30 |
| **Total Production** | **$17,000** | **~$118/month** |

*Based on 1,000 patients, 500 queries/day*

---

## Timeline

```
MVP (Now) ──┬──> Phase 1 (Week 1-2)
            │
            ├──> Phase 2 (Week 3-4) [HIPAA Core]
            │
            ├──> Phase 3 (Week 5-6)
            │
            └──> Phase 4 (Week 7-8) ──> Production Ready ✓
                                         (2 months total)
```

---

## Compliance Checklist

### HIPAA Administrative Safeguards
- [ ] Security Management Process
- [ ] Assigned Security Responsibility
- [ ] Workforce Security
- [ ] Information Access Management
- [ ] Security Awareness and Training
- [ ] Security Incident Procedures
- [ ] Contingency Plan
- [ ] Evaluation
- [ ] Business Associate Contracts

### HIPAA Physical Safeguards
- [x] Facility Access Controls (AWS data centers)
- [x] Workstation Use (AWS managed)
- [x] Workstation Security (AWS managed)
- [x] Device and Media Controls (AWS managed)

### HIPAA Technical Safeguards
- [ ] Access Control (Unique User IDs, Emergency Access)
- [ ] Audit Controls (Log all access)
- [ ] Integrity (Data not altered/destroyed)
- [ ] Person or Entity Authentication (MFA)
- [ ] Transmission Security (Encryption in transit)

---

## Key Takeaways

### For Hackathon (Now)
✅ **Good enough to demo**  
✅ **Shows AWS capabilities**  
✅ **Foundation for production**  
⚠️ **NOT for real patient data**

### For Production (2 months)
✅ **HIPAA compliant**  
✅ **Enterprise security**  
✅ **Audit-ready**  
✅ **Disaster recovery**

---

## Resources

- [AWS HIPAA Compliance](https://aws.amazon.com/compliance/hipaa-compliance/)
- [HealthLake Documentation](https://docs.aws.amazon.com/healthlake/)
- [HIPAA Security Rule](https://www.hhs.gov/hipaa/for-professionals/security/)
- [AWS Well-Architected Framework - Healthcare](https://aws.amazon.com/architecture/well-architected/)

---

**Questions?** Open an issue or contact the compliance team!

