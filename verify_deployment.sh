#!/bin/bash

###############################################################################
# Hospital Multi-Agent System - Deployment Verification Script
###############################################################################

echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║  🔍 Hospital Multi-Agent Deployment Verification             ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test 1: Check AWS Credentials
echo -e "${BLUE}[1/5] Checking AWS Credentials...${NC}"
if aws sts get-caller-identity &> /dev/null; then
    ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
    echo -e "${GREEN}✓ AWS credentials configured (Account: ${ACCOUNT_ID})${NC}"
else
    echo -e "${RED}✗ AWS credentials not configured${NC}"
    exit 1
fi
echo ""

# Test 2: Check DynamoDB Tables
echo -e "${BLUE}[2/5] Checking DynamoDB Tables...${NC}"
for table in "hospital-patients-dev" "hospital-appointments-dev" "hospital-memory-dev"; do
    if aws dynamodb describe-table --table-name $table --region us-east-1 &> /dev/null; then
        count=$(aws dynamodb scan --table-name $table --region us-east-1 --select COUNT --query 'Count' --output text)
        echo -e "${GREEN}✓ ${table} (${count} items)${NC}"
    else
        echo -e "${RED}✗ ${table} not found${NC}"
    fi
done
echo ""

# Test 3: Check Bedrock Model Listing
echo -e "${BLUE}[3/5] Checking Bedrock Model Access...${NC}"
if aws bedrock list-foundation-models --region us-east-1 &> /dev/null; then
    echo -e "${GREEN}✓ Can list Bedrock models${NC}"
else
    echo -e "${RED}✗ Cannot list Bedrock models${NC}"
fi
echo ""

# Test 4: Check Bedrock Model Invocation
echo -e "${BLUE}[4/5] Testing Bedrock Model Invocation...${NC}"
python3 -c "
import boto3
import json
try:
    client = boto3.client('bedrock-runtime', region_name='us-east-1')
    response = client.invoke_model(
        modelId='anthropic.claude-3-5-sonnet-20240620-v1:0',
        body=json.dumps({
            'anthropic_version': 'bedrock-2023-05-31',
            'max_tokens': 10,
            'messages': [{'role': 'user', 'content': 'Hi'}]
        })
    )
    print('${GREEN}✓ Bedrock model invocation working!${NC}')
    exit(0)
except Exception as e:
    if 'AccessDenied' in str(e):
        print('${YELLOW}⚠ Model access not yet enabled${NC}')
        print('${YELLOW}  → Go to: https://us-east-1.console.aws.amazon.com/bedrock/home?region=us-east-1#/modelaccess${NC}')
        print('${YELLOW}  → Enable Claude 3.5 Sonnet model access${NC}')
    else:
        print(f'${RED}✗ Error: {e}${NC}')
    exit(1)
" 2>&1 && echo "" || echo ""

# Test 5: Check Python Dependencies
echo -e "${BLUE}[5/5] Checking Python Dependencies...${NC}"
python3 -c "
import importlib
deps = ['boto3', 'streamlit', 'anthropic']
all_good = True
for dep in deps:
    try:
        importlib.import_module(dep)
        print(f'${GREEN}✓ {dep}${NC}')
    except ImportError:
        print(f'${RED}✗ {dep} not installed${NC}')
        all_good = False
if not all_good:
    print('\n${YELLOW}Run: pip3 install -r requirements.txt${NC}')
"
echo ""

# Summary
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║  📊 Verification Summary                                     ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
echo "If all checks passed, you're ready to run:"
echo -e "${GREEN}  streamlit run ui/streamlit_app.py${NC}"
echo ""
echo "If Bedrock model invocation failed:"
echo -e "${YELLOW}  1. Go to AWS Bedrock Console${NC}"
echo -e "${YELLOW}  2. Enable Claude 3.5 Sonnet model access${NC}"
echo -e "${YELLOW}  3. Run this script again${NC}"
echo ""


