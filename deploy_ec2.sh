#!/bin/bash

###############################################################################
# AWS EC2 Deployment Script
# Deploy Hospital Multi-Agent System to EC2 for 24/7 availability
###############################################################################

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

clear

echo -e "${BLUE}╔═══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                                                               ║${NC}"
echo -e "${BLUE}║     ☁️  AWS EC2 Deployment - Hospital Multi-Agent System     ║${NC}"
echo -e "${BLUE}║                                                               ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Configuration
AWS_REGION=${AWS_REGION:-us-east-1}
INSTANCE_TYPE=${INSTANCE_TYPE:-t2.micro}  # Free tier eligible
KEY_NAME=${KEY_NAME:-hospital-demo-key}
SECURITY_GROUP_NAME="hospital-demo-sg"

# Check prerequisites
echo -e "${YELLOW}[1/6] Checking prerequisites...${NC}"

if ! command -v aws &> /dev/null; then
    echo -e "${RED}✗ AWS CLI not found. Please install it first.${NC}"
    exit 1
fi

if ! aws sts get-caller-identity &> /dev/null; then
    echo -e "${RED}✗ AWS credentials not configured. Run 'aws configure' first.${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Prerequisites met${NC}\n"

# Create security group
echo -e "${YELLOW}[2/6] Creating security group...${NC}"

# Check if security group exists
SG_ID=$(aws ec2 describe-security-groups \
    --filters "Name=group-name,Values=${SECURITY_GROUP_NAME}" \
    --query 'SecurityGroups[0].GroupId' \
    --output text \
    --region ${AWS_REGION} 2>/dev/null)

if [ "$SG_ID" == "None" ] || [ -z "$SG_ID" ]; then
    # Create new security group
    SG_ID=$(aws ec2 create-security-group \
        --group-name ${SECURITY_GROUP_NAME} \
        --description "Security group for Hospital Multi-Agent Demo" \
        --region ${AWS_REGION} \
        --query 'GroupId' \
        --output text)
    
    # Allow SSH (port 22)
    aws ec2 authorize-security-group-ingress \
        --group-id ${SG_ID} \
        --protocol tcp \
        --port 22 \
        --cidr 0.0.0.0/0 \
        --region ${AWS_REGION}
    
    # Allow Streamlit (port 8501)
    aws ec2 authorize-security-group-ingress \
        --group-id ${SG_ID} \
        --protocol tcp \
        --port 8501 \
        --cidr 0.0.0.0/0 \
        --region ${AWS_REGION}
    
    echo -e "${GREEN}✓ Security group created: ${SG_ID}${NC}\n"
else
    echo -e "${GREEN}✓ Using existing security group: ${SG_ID}${NC}\n"
fi

# Create key pair if needed
echo -e "${YELLOW}[3/6] Checking SSH key pair...${NC}"

if [ ! -f ~/.ssh/${KEY_NAME}.pem ]; then
    aws ec2 create-key-pair \
        --key-name ${KEY_NAME} \
        --region ${AWS_REGION} \
        --query 'KeyMaterial' \
        --output text > ~/.ssh/${KEY_NAME}.pem
    
    chmod 400 ~/.ssh/${KEY_NAME}.pem
    echo -e "${GREEN}✓ Key pair created: ~/.ssh/${KEY_NAME}.pem${NC}\n"
else
    echo -e "${GREEN}✓ Using existing key pair${NC}\n"
fi

# Get latest Amazon Linux 2023 AMI
echo -e "${YELLOW}[4/6] Finding latest Amazon Linux AMI...${NC}"

AMI_ID=$(aws ec2 describe-images \
    --owners amazon \
    --filters "Name=name,Values=al2023-ami-2023*-x86_64" \
    --query 'Images | sort_by(@, &CreationDate) | [-1].ImageId' \
    --output text \
    --region ${AWS_REGION})

echo -e "${GREEN}✓ Using AMI: ${AMI_ID}${NC}\n"

# Create user data script
echo -e "${YELLOW}[5/6] Creating EC2 user data script...${NC}"

cat > /tmp/ec2-user-data.sh << 'USERDATA'
#!/bin/bash
# Update system
yum update -y

# Install dependencies
yum install -y python3 python3-pip git

# Install Python packages
pip3 install streamlit boto3 botocore

# Create app directory
mkdir -p /home/ec2-user/hospital-app
cd /home/ec2-user/hospital-app

# Download your app (you'll need to provide the GitHub URL)
echo "App files will be deployed separately"

# Create systemd service
cat > /etc/systemd/system/streamlit.service << 'EOF'
[Unit]
Description=Hospital Multi-Agent Streamlit App
After=network.target

[Service]
Type=simple
User=ec2-user
WorkingDirectory=/home/ec2-user/hospital-app
ExecStart=/usr/local/bin/streamlit run ui/streamlit_app.py --server.port=8501 --server.address=0.0.0.0 --server.headless=true
Restart=always
RestartSec=10
Environment="PATH=/usr/local/bin:/usr/bin:/bin"

[Install]
WantedBy=multi-user.target
EOF

# Service will be started after you deploy the code
USERDATA

echo -e "${GREEN}✓ User data script created${NC}\n"

# Launch EC2 instance
echo -e "${YELLOW}[6/6] Launching EC2 instance...${NC}"

INSTANCE_ID=$(aws ec2 run-instances \
    --image-id ${AMI_ID} \
    --instance-type ${INSTANCE_TYPE} \
    --key-name ${KEY_NAME} \
    --security-group-ids ${SG_ID} \
    --user-data file:///tmp/ec2-user-data.sh \
    --tag-specifications "ResourceType=instance,Tags=[{Key=Name,Value=hospital-demo}]" \
    --region ${AWS_REGION} \
    --query 'Instances[0].InstanceId' \
    --output text)

echo -e "${GREEN}✓ Instance launching: ${INSTANCE_ID}${NC}\n"

# Wait for instance to be running
echo -e "${YELLOW}Waiting for instance to be running (this may take 2-3 minutes)...${NC}"
aws ec2 wait instance-running --instance-ids ${INSTANCE_ID} --region ${AWS_REGION}

# Get public IP
PUBLIC_IP=$(aws ec2 describe-instances \
    --instance-ids ${INSTANCE_ID} \
    --region ${AWS_REGION} \
    --query 'Reservations[0].Instances[0].PublicIpAddress' \
    --output text)

echo -e "${GREEN}✓ Instance is running!${NC}\n"

# Clean up
rm /tmp/ec2-user-data.sh

# Print summary
echo -e "${GREEN}╔═══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║                                                               ║${NC}"
echo -e "${GREEN}║   ✓ EC2 Instance Deployed Successfully!                      ║${NC}"
echo -e "${GREEN}║                                                               ║${NC}"
echo -e "${GREEN}╚═══════════════════════════════════════════════════════════════╝${NC}"
echo ""

echo -e "${BLUE}Instance Details:${NC}"
echo -e "  Instance ID: ${GREEN}${INSTANCE_ID}${NC}"
echo -e "  Public IP: ${GREEN}${PUBLIC_IP}${NC}"
echo -e "  Region: ${GREEN}${AWS_REGION}${NC}"
echo -e "  Instance Type: ${GREEN}${INSTANCE_TYPE}${NC}"
echo ""

echo -e "${BLUE}Next Steps:${NC}"
echo ""
echo -e "${YELLOW}1. SSH into your instance:${NC}"
echo -e "   ${GREEN}ssh -i ~/.ssh/${KEY_NAME}.pem ec2-user@${PUBLIC_IP}${NC}"
echo ""
echo -e "${YELLOW}2. Deploy your application code:${NC}"
echo -e "   ${GREEN}cd /home/ec2-user/hospital-app${NC}"
echo -e "   ${GREEN}git clone <your-github-repo-url> .${NC}"
echo ""
echo -e "${YELLOW}3. Start the Streamlit service:${NC}"
echo -e "   ${GREEN}sudo systemctl start streamlit${NC}"
echo -e "   ${GREEN}sudo systemctl enable streamlit${NC}"
echo ""
echo -e "${YELLOW}4. Access your app:${NC}"
echo -e "   ${BLUE}http://${PUBLIC_IP}:8501${NC}"
echo ""
echo -e "${YELLOW}5. Check service status:${NC}"
echo -e "   ${GREEN}sudo systemctl status streamlit${NC}"
echo ""
echo -e "${BLUE}💰 Cost Estimate:${NC}"
echo -e "   t2.micro (Free tier): ${GREEN}Free for 750 hours/month${NC}"
echo -e "   After free tier: ${YELLOW}~$8-10/month${NC}"
echo ""
echo -e "${YELLOW}To stop the instance (to avoid charges):${NC}"
echo -e "   ${GREEN}aws ec2 stop-instances --instance-ids ${INSTANCE_ID} --region ${AWS_REGION}${NC}"
echo ""
echo -e "${YELLOW}To terminate the instance:${NC}"
echo -e "   ${GREEN}aws ec2 terminate-instances --instance-ids ${INSTANCE_ID} --region ${AWS_REGION}${NC}"
echo ""


