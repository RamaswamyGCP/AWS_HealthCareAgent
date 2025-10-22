# 🚀 Quick Start: Deploy for 24/7 Access

Your app is currently running on `localhost:8501` - here's how to make it accessible anytime without keeping your laptop running:

---

## ⭐ RECOMMENDED: Streamlit Cloud (5 minutes, FREE)

**Perfect for demos and professional presentations**

### Quick Deploy:
```bash
./deploy_streamlit_cloud.sh
```

### Manual Steps:
1. **Push to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Hospital Multi-Agent System"
   git remote add origin https://github.com/YOUR_USERNAME/hospital-multi-agent.git
   git push -u origin main
   ```

2. **Deploy:**
   - Visit: https://share.streamlit.io
   - Click "New app"
   - Select your repo
   - Main file: `ui/streamlit_app.py`
   - Deploy!

3. **Result:**
   - ✅ Permanent URL: `https://your-app.streamlit.app`
   - ✅ Always running 24/7
   - ✅ Free forever
   - ✅ Auto-updates on git push

---

## ☁️ AWS EC2 (15 minutes, $0-10/month)

**For AWS integration and full control**

### Quick Deploy:
```bash
./deploy_ec2.sh
```

This will:
- ✅ Create EC2 instance (t2.micro - free tier)
- ✅ Configure security groups (ports 22, 8501)
- ✅ Set up auto-start service
- ✅ Give you public IP

### After deployment:
1. SSH into instance
2. Clone your code
3. Start Streamlit service
4. Access at: `http://<PUBLIC_IP>:8501`

**Cost:** Free for 750 hours/month (first year), then ~$8-10/month

---

## 🔗 Temporary Sharing (2 minutes, FREE)

**For quick demos while keeping laptop running**

### Option A: ngrok
```bash
# Install
brew install ngrok

# Run (in new terminal)
ngrok http 8501

# Share the URL: https://abc123.ngrok-free.app
```

### Option B: Cloudflare Tunnel
```bash
# Install
brew install cloudflared

# Run
cloudflared tunnel --url http://localhost:8501

# Share the URL provided
```

⚠️ **Note:** These require your laptop to stay running

---

## 📊 Comparison

| Method | Time | Cost | Always On | Best For |
|--------|------|------|-----------|----------|
| **Streamlit Cloud** | 5 min | Free | ✅ | Demos, hackathons |
| **AWS EC2** | 15 min | $0-10/mo | ✅ | Production, AWS integration |
| **ngrok** | 2 min | Free | ⚠️ Need laptop | Quick sharing |
| **Cloudflare** | 2 min | Free | ⚠️ Need laptop | Quick sharing |

---

## 🎯 My Recommendation

**For your use case (professional laptop, access anytime):**

### Best: Streamlit Cloud
```bash
./deploy_streamlit_cloud.sh
# Follow the prompts
# Share permanent URL with team
```

### Alternative: AWS EC2
```bash
./deploy_ec2.sh
# Instance will run 24/7
# Access via public IP
```

---

## 🔐 Important: AWS Credentials

For Streamlit Cloud or EC2 deployment, configure AWS credentials:

### Streamlit Cloud (via Secrets):
```toml
# In Streamlit Cloud UI -> Settings -> Secrets
AWS_ACCESS_KEY_ID = "your-key"
AWS_SECRET_ACCESS_KEY = "your-secret"
AWS_REGION = "us-east-1"
```

### EC2 (via IAM Role - Recommended):
- Attach IAM role with Bedrock permissions to EC2 instance
- No hardcoded credentials needed!

---

## 🆘 Need Help?

Check `DEPLOYMENT_GUIDE.md` for detailed instructions on each option.

**Current Status:** ✅ App running locally on http://localhost:8501

