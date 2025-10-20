# 🎯 Next Steps - Enable Bedrock Access

## ⚡ Quick Action Required (2 minutes)

Your deployment is **80% complete**! You just need to enable Bedrock model access.

### Step-by-Step Guide:

#### 1. Open AWS Bedrock Console
Go to: https://us-east-1.console.aws.amazon.com/bedrock/home?region=us-east-1#/modelaccess

#### 2. Request Model Access
- Click the orange "**Manage model access**" button (or "Request model access")
- Scroll down to find "**Anthropic**"
- Check the box next to "**Claude 3.5 Sonnet**"  
  (Model ID: `anthropic.claude-3-5-sonnet-20240620-v1:0`)
- Scroll to bottom and click "**Save changes**"

#### 3. Wait for Approval
- Usually instant! ⚡
- Status will change from "Available to request" → "**Access granted**"

#### 4. Verify Access
Run this command to verify:
```bash
cd /Users/ramaswamy/Documents/AWSOpenHack/hospital-multi-agent
python3 -c "import boto3, json; client = boto3.client('bedrock-runtime', region_name='us-east-1'); response = client.invoke_model(modelId='anthropic.claude-3-5-sonnet-20240620-v1:0', body=json.dumps({'anthropic_version':'bedrock-2023-05-31','max_tokens':10,'messages':[{'role':'user','content':'Hi'}]})); print('✅ Bedrock access working!')"
```

---

## 🚀 After Bedrock Access is Enabled

### Option A: Run the Streamlit UI (Recommended)
```bash
cd /Users/ramaswamy/Documents/AWSOpenHack/hospital-multi-agent
streamlit run ui/streamlit_app.py
```

Then:
- Open browser to http://localhost:8501
- Select a patient (e.g., Emma Johnson - P12345)
- Try: "My child has fever and cough"
- See the AI agent provide triage recommendations!

### Option B: Run the CLI Agent
```bash
cd /Users/ramaswamy/Documents/AWSOpenHack/hospital-multi-agent
python3 local_agent.py
```

Then:
- Enter patient ID: `P12345`
- Ask: "My child has a fever"
- Get real-time AI responses!

---

## 📊 What's Already Deployed

✅ **DynamoDB Tables**: 3 tables with 5 patients, 3 appointments  
✅ **Mock Data**: Loaded and ready  
✅ **IAM Permissions**: All major policies attached  
✅ **Configuration**: `.env` file created  

⚠️ **Pending**: Bedrock model access (you're about to fix this!)

---

## 🎬 Demo Ready in 5 Minutes!

1. ⏱️ **2 min**: Enable Bedrock model access (see above)
2. ⏱️ **1 min**: Run `streamlit run ui/streamlit_app.py`
3. ⏱️ **2 min**: Test with sample queries
4. ✅ **Ready**: Demo to judges!

---

## 💡 Sample Demo Flow

Once running:

1. **Select Patient**: Emma Johnson (P12345)  
   - Shows: 8-year-old with peanut allergy

2. **Symptom Query**: "My child has fever and cough"  
   - Agent checks allergies automatically
   - Provides urgency assessment
   - Suggests next steps

3. **Booking Query**: "Can I book an appointment?"  
   - Agent shows available slots
   - Books appointment
   - Confirms details

4. **Follow-up**: Ask another question  
   - Agent remembers previous conversation
   - Provides contextual response

**Winning demo! 🏆**

---

## 🆘 If Bedrock Access Takes Too Long

The Streamlit UI has a "Local Mode" toggle:
- Toggle "Local Mode" ON
- Uses simulated responses (no Bedrock needed)
- Still fully functional for demo!

---

## 📞 Help

Having trouble? Check:
- `DEPLOYMENT_STATUS.md` - Full deployment status
- `README.md` - Complete documentation  
- `QUICKSTART.md` - Quick start guide

---

**You're almost there! Enable Bedrock and you're demo-ready! 🚀**
