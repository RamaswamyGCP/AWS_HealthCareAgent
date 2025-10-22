# 🌐 Deployment Guide - Keep Your Demo Running 24/7

## Option 1: Streamlit Cloud (⭐ Recommended - Free & Easy)

**Best for:** Quick demos, professional hackathon presentations

### Steps:
1. **Push your code to GitHub:**
   ```bash
   cd /Users/ramaswamy/Documents/AWSOpenHack/hospital-multi-agent
   git init
   git add .
   git commit -m "Hospital Multi-Agent System"
   git branch -M main
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```

2. **Deploy to Streamlit Cloud:**
   - Go to https://share.streamlit.io
   - Sign in with GitHub
   - Click "New app"
   - Select your repository
   - Set main file path: `ui/streamlit_app.py`
   - Click "Deploy"

3. **You'll get a permanent URL like:**
   `https://your-app-name.streamlit.app`

**Pros:**
- ✅ Completely free
- ✅ Always running (24/7)
- ✅ Auto-updates on git push
- ✅ Professional URL
- ✅ SSL certificate included
- ✅ No infrastructure management

**Cons:**
- ⚠️ Public (anyone with URL can access)
- ⚠️ Limited to 1GB RAM on free tier

---

## Option 2: AWS EC2 (Professional Cloud Hosting)

**Best for:** Full control, AWS integration, production-ready

### Quick Deploy Script:

```bash
# 1. Launch EC2 instance
aws ec2 run-instances \
    --image-id ami-0c55b159cbfafe1f0 \
    --instance-type t2.micro \
    --key-name your-key-name \
    --security-groups default \
    --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=hospital-demo}]'

# 2. SSH into instance
ssh -i your-key.pem ec2-user@<instance-public-ip>

# 3. Setup on EC2
sudo yum update -y
sudo yum install python3 git -y
git clone <your-repo-url>
cd hospital-multi-agent
pip3 install -r requirements.txt

# 4. Run as background service
nohup streamlit run ui/streamlit_app.py --server.port 8501 --server.address 0.0.0.0 &

# 5. Access at: http://<instance-public-ip>:8501
```

**Cost:** ~$0-10/month (free tier eligible)

---

## Option 3: AWS App Runner (Easiest AWS Option)

**Best for:** Serverless, auto-scaling, AWS-native

### Setup:
1. Create `Dockerfile` in project root:
   ```dockerfile
   FROM python:3.11-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   EXPOSE 8501
   CMD ["streamlit", "run", "ui/streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
   ```

2. Deploy via AWS Console or CLI:
   ```bash
   aws apprunner create-service \
       --service-name hospital-multi-agent \
       --source-configuration '{
           "ImageRepository": {
               "ImageIdentifier": "<your-ecr-image>",
               "ImageRepositoryType": "ECR"
           }
       }'
   ```

**Cost:** ~$5-15/month (pay for usage)

---

## Option 4: Run as System Service (On Your Laptop)

**Best for:** Testing, but NOT recommended for "always available"

### Setup systemd service (macOS alternative: launchd):

```bash
# Create service file
cat > ~/Library/LaunchAgents/com.hospital.streamlit.plist << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.hospital.streamlit</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/bin/streamlit</string>
        <string>run</string>
        <string>/Users/ramaswamy/Documents/AWSOpenHack/hospital-multi-agent/ui/streamlit_app.py</string>
        <string>--server.port=8501</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
</dict>
</plist>
EOF

# Load service
launchctl load ~/Library/LaunchAgents/com.hospital.streamlit.plist

# Service will now start automatically on login
```

**Cons:**
- ⚠️ Laptop must stay on and connected
- ⚠️ Only accessible on local network (need ngrok/cloudflare for external access)

---

## 🎯 My Recommendation for Your Use Case

**Use Streamlit Cloud:**
1. Push to GitHub (takes 2 minutes)
2. Deploy on share.streamlit.io (takes 3 minutes)
3. Share permanent URL with your team
4. They can access anytime, anywhere

**Alternative: AWS EC2**
If you need AWS integration and already have infrastructure deployed:
- Deploy to t2.micro (free tier)
- Set up security groups to allow port 8501
- Run streamlit as background service
- Access via public IP

---

## 📋 Quick Comparison

| Option | Cost | Setup Time | Always On | Professional |
|--------|------|------------|-----------|--------------|
| **Streamlit Cloud** | Free | 5 min | ✅ | ⭐⭐⭐⭐⭐ |
| **AWS EC2** | $0-10/mo | 15 min | ✅ | ⭐⭐⭐⭐ |
| **AWS App Runner** | $5-15/mo | 20 min | ✅ | ⭐⭐⭐⭐⭐ |
| **Laptop Service** | Free | 5 min | ⚠️ | ⭐⭐ |
| **ngrok + Laptop** | Free | 2 min | ⚠️ | ⭐⭐⭐ |

---

## 🚀 Next Steps

Choose your deployment method and I can help you set it up!

