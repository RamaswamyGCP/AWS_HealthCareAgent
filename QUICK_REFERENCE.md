# 🚀 Quick Reference - Hospital Multi-Agent System

## 🎯 APPLICATION ACCESS
**Streamlit UI**: http://localhost:8501 ✅ **RUNNING NOW**

---

## 📝 Demo Script (3 minutes)

### 1️⃣ Introduction (30 sec)
"This is a hospital multi-agent AI system using AWS Bedrock Claude 3.5 Sonnet v2. It intelligently routes patient queries to specialized AI agents."

### 2️⃣ Live Demo (2 min)
1. **Select Patient**: Emma Johnson (P12345)
2. **Query 1**: "My child has fever and cough"
   - Shows symptom triage
   - Checks allergies (peanut allergy)
   - Assesses urgency
3. **Query 2**: "Can I book an appointment?"
   - Shows booking flow
   - Checks availability
4. **Query 3**: "What were the symptoms again?"
   - Shows memory/context retention

### 3️⃣ Technical Highlights (30 sec)
- Multi-agent architecture (Supervisor, Triage, Booking, Reminder)
- AWS Bedrock Claude 3.5 Sonnet v2
- DynamoDB for patient data
- Context-aware responses

---

## 🔑 Key Features to Highlight

✅ **Multi-Agent Orchestration**: Supervisor routes to specialized agents  
✅ **Context Awareness**: Remembers patient history and allergies  
✅ **Real-time AI**: Live responses from AWS Bedrock  
✅ **AWS Integration**: DynamoDB, Bedrock, CloudFormation  
✅ **Scalable**: Cloud-native architecture  

---

## 🛠️ Useful Commands

### Restart UI
```bash
pkill -f streamlit
cd /Users/ramaswamy/Documents/AWSOpenHack/hospital-multi-agent
streamlit run ui/streamlit_app.py
```

### Test Agent
```bash
cd /Users/ramaswamy/Documents/AWSOpenHack/hospital-multi-agent
python3 local_agent.py
```

### Check Deployment
```bash
./verify_deployment.sh
```

### View Logs
```bash
# Streamlit logs
tail -f ~/.streamlit/logs/*.log

# AWS CloudFormation
aws cloudformation describe-stacks --stack-name hospital-db-dev --region us-east-1
```

---

## 📊 AWS Resources

| Resource | Name | Items |
|----------|------|-------|
| DynamoDB | hospital-patients-dev | 5 patients |
| DynamoDB | hospital-appointments-dev | 3 appointments |
| DynamoDB | hospital-memory-dev | 2 memory entries |
| Bedrock | Claude 3.5 Sonnet v2 | Active |
| Stack | hospital-db-dev | CREATE_COMPLETE |

---

## 🎤 Presentation Tips

**Opening Hook**: "Healthcare is complex. We built an AI system that makes it simple."

**Problem**: "Patients need quick, accurate health guidance and easy appointment booking."

**Solution**: "Our multi-agent system uses AWS Bedrock to provide intelligent triage, seamless booking, and contextual care."

**Demo**: [Show live interaction]

**Tech**: "Built with AWS Bedrock Claude 3.5 Sonnet v2, DynamoDB, and multi-agent architecture."

**Impact**: "Reduces wait times, improves patient experience, scales with AWS."

---

## ⚡ Quick Troubleshooting

**UI won't load?**
```bash
pkill -f streamlit
streamlit run ui/streamlit_app.py
```

**Bedrock errors?**
- Check: Model access enabled in console
- Model ID: `us.anthropic.claude-3-5-sonnet-20241022-v2:0`

**DynamoDB errors?**
- Tables exist: `aws dynamodb list-tables --region us-east-1`
- Check .env file has correct table names

---

## 💰 Cost Estimate
**2-Day Hackathon**: ~$6 total
- DynamoDB: ~$1
- Bedrock: ~$5
- S3: < $0.01

---

## 📞 Documentation
- `DEPLOYMENT_COMPLETE.md` - Full details
- `README.md` - Complete docs
- `config.yaml` - Configuration

---

## ✅ Pre-Demo Checklist
- [ ] UI running at http://localhost:8501
- [ ] Test with Emma Johnson (P12345)
- [ ] Test symptom query
- [ ] Test booking query
- [ ] Test follow-up (memory)
- [ ] Presentation ready
- [ ] Demo script practiced

---

**🎉 You're ready! Go win that hackathon! 🏆**

