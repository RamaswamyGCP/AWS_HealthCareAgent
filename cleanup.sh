#!/bin/bash

###############################################################################
# Hospital Multi-Agent System - Cleanup Script
# Removes all AWS resources to avoid costs
###############################################################################

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

AWS_REGION=${AWS_REGION:-us-east-1}
ENVIRONMENT=${ENVIRONMENT:-dev}
STACK_NAME="hospital-multi-agent-${ENVIRONMENT}"

echo -e "${RED}"
echo "============================================================"
echo "  Hospital Multi-Agent System - Cleanup"
echo "============================================================"
echo -e "${NC}"

echo -e "${YELLOW}This will delete ALL resources created by the deployment.${NC}"
echo -e "${YELLOW}Stack: ${STACK_NAME}${NC}"
echo -e "${YELLOW}Region: ${AWS_REGION}${NC}"
echo ""

read -p "Are you sure you want to continue? (yes/no): " confirm

if [ "$confirm" != "yes" ]; then
    echo -e "${BLUE}Cleanup cancelled.${NC}"
    exit 0
fi

echo ""
echo -e "${YELLOW}Starting cleanup...${NC}"
echo ""

# Delete CloudFormation Stack
echo -e "${YELLOW}[1/3] Deleting CloudFormation stack...${NC}"

aws cloudformation delete-stack \
    --stack-name ${STACK_NAME} \
    --region ${AWS_REGION}

echo -e "${BLUE}  Waiting for stack deletion...${NC}"
aws cloudformation wait stack-delete-complete \
    --stack-name ${STACK_NAME} \
    --region ${AWS_REGION}

echo -e "${GREEN}✓ Stack deleted${NC}"
echo ""

# Clean up S3 bucket (if exists)
echo -e "${YELLOW}[2/3] Cleaning up S3 buckets...${NC}"

CONFIG_BUCKET="hospital-config-${AWS_ACCOUNT_ID:-unknown}-${ENVIRONMENT}"

if aws s3 ls s3://${CONFIG_BUCKET} 2>/dev/null; then
    echo -e "${BLUE}  Emptying bucket: ${CONFIG_BUCKET}${NC}"
    aws s3 rm s3://${CONFIG_BUCKET} --recursive --region ${AWS_REGION}
    
    echo -e "${BLUE}  Deleting bucket: ${CONFIG_BUCKET}${NC}"
    aws s3 rb s3://${CONFIG_BUCKET} --region ${AWS_REGION}
    
    echo -e "${GREEN}✓ S3 bucket cleaned${NC}"
else
    echo -e "${BLUE}  No S3 bucket found${NC}"
fi

echo ""

# Clean up local files
echo -e "${YELLOW}[3/3] Cleaning up local files...${NC}"

rm -f .env
rm -rf infrastructure/.aws-sam

echo -e "${GREEN}✓ Local files cleaned${NC}"
echo ""

echo -e "${GREEN}"
echo "============================================================"
echo "  ✓ Cleanup Complete!"
echo "============================================================"
echo -e "${NC}"
echo ""
echo -e "${BLUE}All AWS resources have been removed.${NC}"
echo ""

