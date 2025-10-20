#!/bin/bash

###############################################################################
# Hospital Multi-Agent System - Deployment Script
# Fast-track deployment for AWS Hackathon
###############################################################################

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
AWS_REGION=${AWS_REGION:-us-east-1}
ENVIRONMENT=${ENVIRONMENT:-dev}
STACK_NAME="hospital-multi-agent-${ENVIRONMENT}"

echo -e "${BLUE}"
echo "============================================================"
echo "  Hospital Multi-Agent System - Deployment"
echo "============================================================"
echo -e "${NC}"

# Step 1: Check Prerequisites
echo -e "${YELLOW}[1/7] Checking prerequisites...${NC}"

# Check AWS CLI
if ! command -v aws &> /dev/null; then
    echo -e "${RED}✗ AWS CLI not found. Please install it first.${NC}"
    exit 1
fi
echo -e "${GREEN}✓ AWS CLI found${NC}"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}✗ Python 3 not found. Please install it first.${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Python 3 found${NC}"

# Check SAM CLI
if ! command -v sam &> /dev/null; then
    echo -e "${YELLOW}⚠ SAM CLI not found. Installing...${NC}"
    pip3 install aws-sam-cli
fi
echo -e "${GREEN}✓ SAM CLI ready${NC}"

# Check AWS credentials
if ! aws sts get-caller-identity &> /dev/null; then
    echo -e "${RED}✗ AWS credentials not configured. Run 'aws configure' first.${NC}"
    exit 1
fi
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
echo -e "${GREEN}✓ AWS credentials configured (Account: ${AWS_ACCOUNT_ID})${NC}"

# Check Bedrock access
echo -e "${YELLOW}  Checking Bedrock model access...${NC}"
if aws bedrock list-foundation-models --region ${AWS_REGION} &> /dev/null; then
    echo -e "${GREEN}✓ Bedrock access confirmed${NC}"
else
    echo -e "${YELLOW}⚠ Unable to verify Bedrock access. Ensure you have permissions.${NC}"
fi

echo ""

# Step 2: Install Dependencies
echo -e "${YELLOW}[2/7] Installing Python dependencies...${NC}"
pip3 install -q -r requirements.txt
echo -e "${GREEN}✓ Dependencies installed${NC}"
echo ""

# Step 3: Build SAM Application
echo -e "${YELLOW}[3/7] Building SAM application...${NC}"
cd infrastructure
sam build --use-container || sam build
echo -e "${GREEN}✓ SAM build complete${NC}"
echo ""

# Step 4: Deploy Infrastructure
echo -e "${YELLOW}[4/7] Deploying infrastructure to AWS...${NC}"
echo -e "${BLUE}  Stack Name: ${STACK_NAME}${NC}"
echo -e "${BLUE}  Region: ${AWS_REGION}${NC}"
echo -e "${BLUE}  Environment: ${ENVIRONMENT}${NC}"
echo ""

sam deploy \
    --stack-name ${STACK_NAME} \
    --region ${AWS_REGION} \
    --capabilities CAPABILITY_IAM \
    --parameter-overrides \
        Environment=${ENVIRONMENT} \
    --no-confirm-changeset \
    --no-fail-on-empty-changeset

echo -e "${GREEN}✓ Infrastructure deployed${NC}"
echo ""

# Step 5: Get Stack Outputs
echo -e "${YELLOW}[5/7] Retrieving stack outputs...${NC}"

PATIENTS_TABLE=$(aws cloudformation describe-stacks \
    --stack-name ${STACK_NAME} \
    --region ${AWS_REGION} \
    --query "Stacks[0].Outputs[?OutputKey=='PatientsTableName'].OutputValue" \
    --output text)

APPOINTMENTS_TABLE=$(aws cloudformation describe-stacks \
    --stack-name ${STACK_NAME} \
    --region ${AWS_REGION} \
    --query "Stacks[0].Outputs[?OutputKey=='AppointmentsTableName'].OutputValue" \
    --output text)

MEMORY_TABLE=$(aws cloudformation describe-stacks \
    --stack-name ${STACK_NAME} \
    --region ${AWS_REGION} \
    --query "Stacks[0].Outputs[?OutputKey=='MemoryTableName'].OutputValue" \
    --output text)

API_ENDPOINT=$(aws cloudformation describe-stacks \
    --stack-name ${STACK_NAME} \
    --region ${AWS_REGION} \
    --query "Stacks[0].Outputs[?OutputKey=='ApiEndpoint'].OutputValue" \
    --output text)

CONFIG_BUCKET=$(aws cloudformation describe-stacks \
    --stack-name ${STACK_NAME} \
    --region ${AWS_REGION} \
    --query "Stacks[0].Outputs[?OutputKey=='ConfigBucketName'].OutputValue" \
    --output text)

echo -e "${GREEN}✓ Stack outputs retrieved${NC}"
echo ""

# Step 6: Load Mock Data
echo -e "${YELLOW}[6/7] Loading mock patient data...${NC}"
cd ../data

export AWS_REGION=${AWS_REGION}
export PATIENTS_TABLE=${PATIENTS_TABLE}
export APPOINTMENTS_TABLE=${APPOINTMENTS_TABLE}
export MEMORY_TABLE=${MEMORY_TABLE}

python3 load_mock_data.py

echo -e "${GREEN}✓ Mock data loaded${NC}"
echo ""

# Step 7: Deploy Agent to Bedrock AgentCore
echo -e "${YELLOW}[7/7] Setting up Bedrock AgentCore...${NC}"
cd ..

# Create .env file for local testing
cat > .env << EOF
AWS_REGION=${AWS_REGION}
AWS_ACCOUNT_ID=${AWS_ACCOUNT_ID}
PATIENTS_TABLE=${PATIENTS_TABLE}
APPOINTMENTS_TABLE=${APPOINTMENTS_TABLE}
MEMORY_TABLE=${MEMORY_TABLE}
API_GATEWAY_URL=${API_ENDPOINT}
BEDROCK_MODEL_ID=anthropic.claude-3-5-sonnet-20240620-v1:0
LOCAL_MODE=false
EOF

echo -e "${GREEN}✓ Environment configured${NC}"
echo ""

# Configure AgentCore (if toolkit is available)
if command -v agentcore &> /dev/null; then
    echo -e "${BLUE}  Configuring Bedrock AgentCore...${NC}"
    
    agentcore configure \
        -e agents/hospital_agent.py \
        --region ${AWS_REGION} || true
    
    echo -e "${BLUE}  Launching agent to AgentCore Runtime...${NC}"
    agentcore launch || echo -e "${YELLOW}⚠ AgentCore launch skipped. Deploy manually if needed.${NC}"
else
    echo -e "${YELLOW}⚠ AgentCore CLI not found. Skip this for MVP or install toolkit:${NC}"
    echo -e "${BLUE}  pip install bedrock-agentcore-starter-toolkit${NC}"
fi

echo ""

# Deployment Summary
echo -e "${GREEN}"
echo "============================================================"
echo "  ✓ Deployment Complete!"
echo "============================================================"
echo -e "${NC}"
echo ""
echo -e "${BLUE}Resources Created:${NC}"
echo -e "  • DynamoDB Tables:"
echo -e "    - Patients: ${PATIENTS_TABLE}"
echo -e "    - Appointments: ${APPOINTMENTS_TABLE}"
echo -e "    - Memory: ${MEMORY_TABLE}"
echo -e "  • API Gateway: ${API_ENDPOINT}"
echo -e "  • S3 Config Bucket: ${CONFIG_BUCKET}"
echo ""
echo -e "${BLUE}Next Steps:${NC}"
echo -e "  1. Test the agent locally:"
echo -e "     ${GREEN}python3 agents/hospital_agent.py${NC}"
echo -e ""
echo -e "  2. Start the UI:"
echo -e "     ${GREEN}streamlit run ui/streamlit_app.py${NC}"
echo -e ""
echo -e "  3. Test with curl:"
echo -e "     ${GREEN}curl -X POST http://localhost:8080/invocations \\${NC}"
echo -e "     ${GREEN}  -H 'Content-Type: application/json' \\${NC}"
echo -e "     ${GREEN}  -d '{\"prompt\": \"My child has fever\", \"patient_id\": \"P12345\"}'${NC}"
echo -e ""
echo -e "${BLUE}Cleanup (after hackathon):${NC}"
echo -e "  ${YELLOW}./cleanup.sh${NC}"
echo ""
echo -e "${GREEN}Happy Hacking! 🚀${NC}"

