#!/bin/bash

###############################################################################
# Streamlit Cloud Deployment Helper
# Prepares your app for Streamlit Cloud deployment
###############################################################################

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

clear

echo -e "${BLUE}╔═══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                                                               ║${NC}"
echo -e "${BLUE}║     🌐 Streamlit Cloud Deployment Setup                      ║${NC}"
echo -e "${BLUE}║                                                               ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Check if git is initialized
if [ ! -d .git ]; then
    echo -e "${YELLOW}[1/4] Initializing Git repository...${NC}"
    git init
    git branch -M main
    echo -e "${GREEN}✓ Git initialized${NC}\n"
else
    echo -e "${GREEN}✓ Git already initialized${NC}\n"
fi

# Create .gitignore if not exists
if [ ! -f .gitignore ]; then
    echo -e "${YELLOW}[2/4] Creating .gitignore...${NC}"
    cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/

# Environment
.env
*.env

# IDE
.vscode/
.idea/
*.swp
*.swo

# Mac
.DS_Store

# Logs
logs/
*.log

# Streamlit
.streamlit/secrets.toml
EOF
    echo -e "${GREEN}✓ .gitignore created${NC}\n"
else
    echo -e "${GREEN}✓ .gitignore exists${NC}\n"
fi

# Create Streamlit config for cloud deployment
echo -e "${YELLOW}[3/4] Creating Streamlit Cloud config...${NC}"
mkdir -p .streamlit

cat > .streamlit/config.toml << 'EOF'
[server]
port = 8501
headless = true
enableCORS = false
enableXsrfProtection = true

[theme]
primaryColor = "#FF6B6B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"

[browser]
gatherUsageStats = false
EOF

echo -e "${GREEN}✓ Streamlit config created${NC}\n"

# Check if requirements.txt is up to date
echo -e "${YELLOW}[4/4] Verifying requirements.txt...${NC}"
if [ -f requirements.txt ]; then
    echo -e "${GREEN}✓ requirements.txt exists${NC}\n"
else
    echo -e "${YELLOW}⚠ Creating requirements.txt...${NC}"
    cat > requirements.txt << 'EOF'
streamlit>=1.28.0
boto3>=1.28.0
botocore>=1.31.0
EOF
    echo -e "${GREEN}✓ requirements.txt created${NC}\n"
fi

# Stage all files
git add .

echo -e "${GREEN}╔═══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║                                                               ║${NC}"
echo -e "${GREEN}║   ✓ Setup Complete! Ready for Streamlit Cloud               ║${NC}"
echo -e "${GREEN}║                                                               ║${NC}"
echo -e "${GREEN}╚═══════════════════════════════════════════════════════════════╝${NC}"
echo ""

echo -e "${BLUE}Next Steps:${NC}"
echo ""
echo -e "${YELLOW}1. Commit your changes:${NC}"
echo -e "   ${GREEN}git commit -m \"Prepare for Streamlit Cloud deployment\"${NC}"
echo ""
echo -e "${YELLOW}2. Create a GitHub repository and push:${NC}"
echo -e "   ${GREEN}git remote add origin https://github.com/yourusername/hospital-multi-agent.git${NC}"
echo -e "   ${GREEN}git push -u origin main${NC}"
echo ""
echo -e "${YELLOW}3. Deploy to Streamlit Cloud:${NC}"
echo -e "   • Visit: ${BLUE}https://share.streamlit.io${NC}"
echo -e "   • Click 'New app'"
echo -e "   • Select your GitHub repository"
echo -e "   • Main file: ${GREEN}ui/streamlit_app.py${NC}"
echo -e "   • Click 'Deploy!'"
echo ""
echo -e "${YELLOW}4. Configure AWS credentials (in Streamlit Cloud):${NC}"
echo -e "   • Go to app settings"
echo -e "   • Add secrets (TOML format):"
echo -e "   ${GREEN}AWS_ACCESS_KEY_ID = \"your-key\"${NC}"
echo -e "   ${GREEN}AWS_SECRET_ACCESS_KEY = \"your-secret\"${NC}"
echo -e "   ${GREEN}AWS_REGION = \"us-east-1\"${NC}"
echo ""
echo -e "${BLUE}Your app will be live at: ${GREEN}https://your-app-name.streamlit.app${NC}"
echo ""
echo -e "${YELLOW}💡 Tip: Make your GitHub repo public for free Streamlit hosting!${NC}"
echo ""

