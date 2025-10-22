# 🔐 Streamlit Cloud AWS Setup Guide

## Problem: App Running in "Offline Mode"

Your app is deployed but showing **"Note: Using offline mode."** because it can't access AWS Bedrock.

---

## ✅ Solution: Add AWS Credentials to Streamlit Cloud

### Step 1: Get Your AWS Credentials

If you don't have AWS credentials yet:

```bash
# Option 1: Use your existing AWS credentials
cat ~/.aws/credentials

# Option 2: Create new IAM user credentials
# Go to AWS Console → IAM → Users → Create User
# Attach policy: AmazonBedrockFullAccess
# Create access key → Save the credentials
```

### Step 2: Add Secrets to Streamlit Cloud

1. **Go to your Streamlit Cloud app**
   - Visit: https://share.streamlit.io/
   - Find your deployed app: `awshealthcareagent-multiagent`

2. **Open App Settings**
   - Click the hamburger menu (⋮) on your app
   - Select **"Settings"**

3. **Add Secrets**
   - Click the **"Secrets"** tab
   - Paste the following (replace with YOUR credentials):

```toml
AWS_ACCESS_KEY_ID = "AKIAXXXXXXXXXXXXXXXX"
AWS_SECRET_ACCESS_KEY = "your-secret-key-here"
AWS_REGION = "us-east-1"
AWS_DEFAULT_REGION = "us-east-1"
```

4. **Save**
   - Click **"Save"** button
   - Your app will automatically restart

5. **Wait 30-60 seconds**
   - The app will redeploy with the new credentials
   - Refresh your browser

---

## ✅ Verification

After adding credentials:

1. Send a test message: **"My child has fever"**
2. Look for: **"✅ Powered by AWS Bedrock (Claude 3.5 Sonnet)"**
3. You should NOT see: ~~"Note: Using offline mode."~~

---

## 🔒 Security Best Practices

### ⚠️ IMPORTANT: Create a Dedicated IAM User

For production, don't use your main AWS credentials:

1. **Create IAM User:**
   ```
   AWS Console → IAM → Users → Add User
   Name: streamlit-bedrock-user
   Access: Programmatic access
   ```

2. **Attach Minimal Policy:**
   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Action": [
           "bedrock:InvokeModel",
           "bedrock:InvokeModelWithResponseStream"
         ],
         "Resource": "arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-3-5-sonnet-20240620-v1:0"
       }
     ]
   }
   ```

3. **Use Those Credentials in Streamlit**

---

## 🐛 Troubleshooting

### Issue: Still showing "offline mode" after adding credentials

**Solution:**
1. Check credentials are correct (no extra spaces)
2. Verify AWS region is `us-east-1`
3. Ensure Bedrock model access is enabled:
   - Go to AWS Console → Bedrock → Model Access
   - Request access to: **Anthropic Claude 3.5 Sonnet**
   - Wait for approval (usually instant)

### Issue: "AccessDeniedException"

**Solution:**
- Your IAM user needs `bedrock:InvokeModel` permission
- Attach policy: `AmazonBedrockFullAccess`

### Issue: "ThrottlingException"

**Solution:**
- This is normal during high usage
- The app has built-in retry logic
- Wait 30 seconds and try again

---

## 📋 Quick Checklist

- [ ] AWS credentials added to Streamlit Cloud Secrets
- [ ] Bedrock model access enabled (Claude 3.5 Sonnet)
- [ ] App restarted (automatic after saving secrets)
- [ ] Tested with a sample query
- [ ] Verified "Powered by AWS Bedrock" message appears

---

## 🎯 Expected Behavior After Setup

### ✅ Working (Online Mode):
```
User: "My child has fever"
AI: [Intelligent response about symptoms]
✅ Powered by AWS Bedrock (Claude 3.5 Sonnet)
```

### ❌ Not Working (Offline Mode):
```
User: "My child has fever"
AI: [Generic canned response]
Note: Using offline mode.
```

---

## 🆘 Still Having Issues?

1. **Check CloudWatch Logs:**
   - Streamlit Cloud → Your App → Logs tab
   - Look for AWS-related errors

2. **Test AWS Credentials Locally:**
   ```bash
   aws bedrock list-foundation-models --region us-east-1
   ```

3. **Verify IAM Permissions:**
   ```bash
   aws iam get-user
   aws iam list-attached-user-policies --user-name YOUR_USERNAME
   ```

---

## 📝 Summary

Your app is currently running in **mock/offline mode** because it can't authenticate with AWS Bedrock. 

**Add your AWS credentials to Streamlit Cloud Secrets** to enable real AI responses powered by Claude 3.5 Sonnet!

---

**Your App URL:** https://awshealthcareagent-multiagent.streamlit.app

