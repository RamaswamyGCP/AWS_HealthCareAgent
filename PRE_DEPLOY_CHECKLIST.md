# 🚀 Pre-Deployment Checklist

## ✅ Prerequisites Installed
- [x] Python 3.12+ ✓
- [x] AWS CLI ✓
- [x] SAM CLI ✓
- [x] Dependencies installed ✓

## 🔐 AWS Configuration

### Step 1: Configure AWS Credentials
```bash
aws configure
```

Enter:
- **AWS Access Key ID**: [From AWS Console → IAM → Users → Security credentials]
- **AWS Secret Access Key**: [Your secret key]
- **Default region**: `us-east-1`
- **Default output format**: `json`

### Step 2: Verify Configuration
```bash
aws sts get-caller-identity
```

Expected output:
```json
{
    "UserId": "AIDXXXXXXXXXXXXXXXXX",
    "Account": "123456789012",
    "Arn": "arn:aws:iam::123456789012:user/yourname"
}
```

### Step 3: Enable Bedrock Model Access

**IMPORTANT**: You must enable Claude 3.5 Sonnet in AWS Bedrock before deployment!

1. Go to [AWS Console](https://console.aws.amazon.com/)
2. Navigate to **Amazon Bedrock**
3. Click **Model Access** in the left sidebar
4. Click **Request Access** or **Manage Model Access**
5. Find **Anthropic Claude 3.5 Sonnet v2** 
6. Check the box next to it
7. Click **Request model access** at the bottom
8. Wait for approval (usually instant!)

### Step 4: Verify Bedrock Access
```bash
aws bedrock list-foundation-models --region us-east-1 --query 'modelSummaries[?contains(modelName, `Claude`) == `true`].modelId' --output table
```

You should see models like:
- `anthropic.claude-3-5-sonnet-20240620-v1:0` ✅ (We need this one!)
- `anthropic.claude-3-sonnet-20240229-v1:0`
- etc.

## 📋 Ready to Deploy?

Once you've completed all steps above, you're ready to deploy!

### Quick Deploy Command
```bash
cd /Users/ramaswamy/Documents/AWSOpenHack/hospital-multi-agent
./deploy.sh
```

### Or Manual Deployment
```bash
cd /Users/ramaswamy/Documents/AWSOpenHack/hospital-multi-agent

# Install dependencies
pip3 install -r requirements.txt

# Deploy infrastructure
cd infrastructure
sam build
sam deploy --guided

# Load mock data
cd ../data
python3 load_mock_data.py

# Test
cd ..
streamlit run ui/streamlit_app.py
```

## 🎯 What Gets Deployed

| Resource | Purpose | Cost |
|----------|---------|------|
| DynamoDB Tables (3) | Patient data, appointments, memory | ~$1/2 days |
| Lambda Functions (3) | Agent tools | < $1 |
| API Gateway | HTTP endpoints | < $1 |
| S3 Bucket | Configs, logs | < $1 |
| CloudWatch Logs | Monitoring | Free tier |
| Bedrock API Calls | Claude 3.5 Sonnet | ~$5/2 days |
| **Total Estimated** | | **~$8 for hackathon** |

## 🐛 Troubleshooting

### "Access Denied" Errors
- **Solution**: Verify IAM permissions. Your user needs:
  - `AmazonDynamoDBFullAccess`
  - `AWSLambda_FullAccess`
  - `AmazonAPIGatewayAdministrator`
  - `AmazonS3FullAccess`
  - `BedrockFullAccess`
  - `CloudFormationFullAccess`

### "Model Not Accessible"
- **Solution**: Enable model access in Bedrock console (see Step 3 above)

### "Stack Already Exists"
- **Solution**: Delete old stack first:
  ```bash
  aws cloudformation delete-stack --stack-name hospital-multi-agent-dev --region us-east-1
  ```

## ✅ Post-Deployment

After deployment completes:

1. **Note the outputs** from CloudFormation:
   - Patients Table Name
   - Appointments Table Name
   - Memory Table Name
   - API Gateway URL

2. **Test the deployment**:
   ```bash
   ./test_agent.sh
   ```

3. **Launch the UI**:
   ```bash
   streamlit run ui/streamlit_app.py
   ```

4. **Try a test query**:
   - Select patient: Emma Johnson (P12345)
   - Type: "My child has fever and cough"
   - Verify: Agent recalls allergies and provides triage

## 🎬 Ready to Demo!

Once everything is deployed and tested, you're ready for the hackathon presentation!

---

**Questions?** Check [README.md](README.md) or [QUICKSTART.md](QUICKSTART.md)

