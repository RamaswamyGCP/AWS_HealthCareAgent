# 🚀 Quick Start Guide

Get the Hospital Multi-Agent System running in **10 minutes**!

---

## Option 1: Full AWS Deployment (Recommended for Hackathon)

### Prerequisites Check
```bash
# Check AWS credentials
aws sts get-caller-identity

# Check Bedrock access
aws bedrock list-foundation-models --region us-east-1 | grep claude

# Install dependencies
pip install -r requirements.txt
```

### Deploy Everything
```bash
chmod +x deploy.sh
./deploy.sh
```

**What this does:**
1. Creates DynamoDB tables
2. Deploys Lambda functions
3. Sets up API Gateway
4. Loads mock patient data
5. Configures Bedrock AgentCore

**Time: 5-8 minutes**

### Test Deployment
```bash
# Test with curl
./test_agent.sh

# Or start UI
streamlit run ui/streamlit_app.py
```

---

## Option 2: Local Development (Fastest for Testing)

### Step 1: Setup Environment
```bash
# Create .env file
cat > .env << EOF
AWS_REGION=us-east-1
PATIENTS_TABLE=hospital-patients-dev
APPOINTMENTS_TABLE=hospital-appointments-dev
MEMORY_TABLE=hospital-memory-dev
BEDROCK_MODEL_ID=anthropic.claude-3-5-sonnet-20240620-v1:0
LOCAL_MODE=true
EOF

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Create Local DynamoDB Tables
```bash
# Install DynamoDB Local
docker run -d -p 8000:8000 amazon/dynamodb-local

# Or skip and use mock data (agent will fall back to mock)
```

### Step 3: Start Agent
```bash
python3 agents/hospital_agent.py
```

### Step 4: Test
```bash
# Terminal 2
curl -X POST http://localhost:8080/invocations \
  -H "Content-Type: application/json" \
  -d '{"prompt": "My child has fever", "patient_id": "P12345"}'
```

### Step 5: Launch UI
```bash
streamlit run ui/streamlit_app.py
```

**Time: 3-5 minutes**

---

## Option 3: UI-Only Demo (No Backend)

Perfect for **presentation mode** when backend isn't available.

```bash
# Just start the UI
streamlit run ui/streamlit_app.py

# Enable "Local Testing Mode" in sidebar
# UI will show mock responses
```

**Time: 1 minute**

---

## 🧪 Quick Test Commands

### Test 1: Symptom Triage
```bash
curl -X POST http://localhost:8080/invocations \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "My child has high fever and cough. What should I do?",
    "patient_id": "P12345"
  }' | jq '.result'
```

### Test 2: Book Appointment
```bash
curl -X POST http://localhost:8080/invocations \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Book appointment for next Tuesday at 2pm",
    "patient_id": "P12346"
  }' | jq '.result'
```

### Test 3: Get Reminders
```bash
curl -X POST http://localhost:8080/invocations \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Show my upcoming appointments",
    "patient_id": "P12347"
  }' | jq '.result'
```

---

## 🎯 Demo Patients Available

| Patient ID | Name | Conditions | Best For Testing |
|-----------|------|------------|------------------|
| P12345 | Emma Johnson | Asthma, Allergies | Pediatric triage |
| P12346 | Michael Chen | Diabetes, Hypertension | Chronic care |
| P12347 | Sarah Williams | Healthy | General booking |
| P12348 | David Martinez | Heart Disease | Urgent triage |
| P12349 | Olivia Brown | Healthy child | Pediatrics |

---

## 🐛 Troubleshooting

### "Connection refused"
```bash
# Check if agent is running
ps aux | grep hospital_agent

# Restart agent
python3 agents/hospital_agent.py
```

### "Model access denied"
```bash
# Enable model in Bedrock console
# AWS Console > Bedrock > Model Access > Request Access
# Select: Anthropic Claude 3.5 Sonnet
```

### "Table not found"
```bash
# Check tables exist
aws dynamodb list-tables --region us-east-1

# Or set LOCAL_MODE=true in .env to use mock data
```

### "SAM build failed"
```bash
# Try without Docker
cd infrastructure
sam build --no-use-container
sam deploy --guided
```

---

## 🎬 Ready to Demo?

1. **Start agent**: `python3 agents/hospital_agent.py`
2. **Start UI**: `streamlit run ui/streamlit_app.py`
3. **Open browser**: `http://localhost:8501`
4. **Select patient**: Emma Johnson (P12345)
5. **Type**: "My child has fever and cough"
6. **Show**: Agent recalls allergies, provides triage
7. **Continue**: "Should I book an appointment?"
8. **Show**: Multi-turn context, booking flow

**Total demo time: 3 minutes**

---

## 🧹 Cleanup After Hackathon

```bash
# Delete all AWS resources
./cleanup.sh

# Removes:
# - DynamoDB tables
# - Lambda functions
# - API Gateway
# - S3 buckets
# - CloudFormation stack
```

---

## 📞 Need Help?

- **Agent not starting?** Check `requirements.txt` installed
- **AWS errors?** Verify credentials: `aws sts get-caller-identity`
- **UI issues?** Try: `pip install --upgrade streamlit`
- **Still stuck?** Open an issue!

---

<div align="center">

**Ready? Let's build! 🚀**

[← Back to README](README.md)

</div>

