#!/bin/bash

###############################################################################
# Hospital Multi-Agent System - Demo Launcher
# Quick start script for hackathon demo
###############################################################################

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

clear

echo -e "${BLUE}"
cat << "EOF"
╔═══════════════════════════════════════════════════════════════╗
║                                                                 ║
║     🏥 HOSPITAL MULTI-AGENT AI SYSTEM                          ║
║                                                                 ║
║     Powered by AWS Bedrock + Strands Agents                    ║
║                                                                 ║
╚═══════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}\n"

# Check if Streamlit is running
if lsof -Pi :8501 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo -e "${GREEN}✓ Streamlit is already running!${NC}\n"
    echo -e "${BLUE}📱 Open in your browser:${NC}"
    echo -e "   ${GREEN}http://localhost:8501${NC}\n"
    
    echo -e "${YELLOW}To restart Streamlit:${NC}"
    echo -e "   1. Press Ctrl+C to stop this script"
    echo -e "   2. Run: ${GREEN}lsof -ti:8501 | xargs kill -9${NC}"
    echo -e "   3. Run: ${GREEN}./START_DEMO.sh${NC}\n"
    
    # Keep script running
    echo -e "${BLUE}Press Ctrl+C to exit...${NC}\n"
    tail -f /dev/null
else
    echo -e "${YELLOW}Starting Hospital Multi-Agent System...${NC}\n"
    
    # Change to project directory
    cd /Users/ramaswamy/Documents/AWSOpenHack/hospital-multi-agent
    
    # Check AWS credentials
    echo -e "${BLUE}[1/3] Checking AWS credentials...${NC}"
    if aws sts get-caller-identity >/dev/null 2>&1; then
        ACCOUNT=$(aws sts get-caller-identity --query Account --output text)
        echo -e "${GREEN}✓ AWS configured (Account: ${ACCOUNT})${NC}\n"
    else
        echo -e "${YELLOW}⚠ AWS credentials not configured${NC}"
        echo -e "   Note: UI will use mock data mode\n"
    fi
    
    # Check dependencies
    echo -e "${BLUE}[2/3] Checking dependencies...${NC}"
    if python3 -c "import streamlit" 2>/dev/null; then
        echo -e "${GREEN}✓ All dependencies installed${NC}\n"
    else
        echo -e "${YELLOW}Installing dependencies...${NC}"
        pip3 install -q -r requirements.txt
        echo -e "${GREEN}✓ Dependencies installed${NC}\n"
    fi
    
    # Start Streamlit
    echo -e "${BLUE}[3/3] Launching Streamlit UI...${NC}\n"
    echo -e "${GREEN}╔═══════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║                                                           ║${NC}"
    echo -e "${GREEN}║   🚀 Demo is starting!                                    ║${NC}"
    echo -e "${GREEN}║                                                           ║${NC}"
    echo -e "${GREEN}║   📱 Open in your browser:                                ║${NC}"
    echo -e "${GREEN}║      http://localhost:8501                                ║${NC}"
    echo -e "${GREEN}║                                                           ║${NC}"
    echo -e "${GREEN}║   👥 Test Patients Available:                             ║${NC}"
    echo -e "${GREEN}║      • Emma Johnson (P12345) - Pediatric                  ║${NC}"
    echo -e "${GREEN}║      • Michael Chen (P12346) - Diabetic                   ║${NC}"
    echo -e "${GREEN}║      • Sarah Williams (P12347) - Healthy                  ║${NC}"
    echo -e "${GREEN}║                                                           ║${NC}"
    echo -e "${GREEN}║   🎯 Try These Queries:                                   ║${NC}"
    echo -e "${GREEN}║      • My child has fever and cough                       ║${NC}"
    echo -e "${GREEN}║      • Book appointment for next week                     ║${NC}"
    echo -e "${GREEN}║      • Show my upcoming reminders                         ║${NC}"
    echo -e "${GREEN}║                                                           ║${NC}"
    echo -e "${GREEN}║   Press Ctrl+C to stop                                    ║${NC}"
    echo -e "${GREEN}║                                                           ║${NC}"
    echo -e "${GREEN}╚═══════════════════════════════════════════════════════════╝${NC}\n"
    
    # Launch Streamlit
    streamlit run ui/streamlit_app.py --server.port 8501 --server.headless true
fi


