#!/bin/bash

###############################################################################
# Hospital Multi-Agent System - Test Script
# Quick testing of the deployed agent
###############################################################################

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

ENDPOINT=${1:-http://localhost:8080/invocations}

echo -e "${BLUE}"
echo "============================================================"
echo "  Hospital Multi-Agent System - Test Suite"
echo "============================================================"
echo -e "${NC}"
echo ""
echo -e "${YELLOW}Testing endpoint: ${ENDPOINT}${NC}"
echo ""

# Test 1: Symptom Triage
echo -e "${BLUE}[Test 1/5] Symptom Triage${NC}"
curl -X POST ${ENDPOINT} \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "My child Emma has high fever (102°F) and severe cough for 3 days. Should I be worried?",
    "patient_id": "P12345"
  }' | jq '.'
echo -e "\n${GREEN}✓ Test 1 complete${NC}\n"
sleep 2

# Test 2: Appointment Booking
echo -e "${BLUE}[Test 2/5] Appointment Booking${NC}"
curl -X POST ${ENDPOINT} \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "I need to book an appointment for next Tuesday afternoon in Pediatrics",
    "patient_id": "P12345"
  }' | jq '.'
echo -e "\n${GREEN}✓ Test 2 complete${NC}\n"
sleep 2

# Test 3: Check Availability
echo -e "${BLUE}[Test 3/5] Check Availability${NC}"
curl -X POST ${ENDPOINT} \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "What appointments are available for Cardiology next week?",
    "patient_id": "P12348"
  }' | jq '.'
echo -e "\n${GREEN}✓ Test 3 complete${NC}\n"
sleep 2

# Test 4: Reminders
echo -e "${BLUE}[Test 4/5] Reminder Management${NC}"
curl -X POST ${ENDPOINT} \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Show me my upcoming appointments and reminders",
    "patient_id": "P12346"
  }' | jq '.'
echo -e "\n${GREEN}✓ Test 4 complete${NC}\n"
sleep 2

# Test 5: Multi-turn Context
echo -e "${BLUE}[Test 5/5] Multi-turn Context (Memory)${NC}"
curl -X POST ${ENDPOINT} \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "I have chest pain",
    "patient_id": "P12348"
  }' | jq '.'
echo ""
sleep 2

curl -X POST ${ENDPOINT} \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Should I go to the ER?",
    "patient_id": "P12348"
  }' | jq '.'
echo -e "\n${GREEN}✓ Test 5 complete${NC}\n"

echo -e "${GREEN}"
echo "============================================================"
echo "  ✓ All Tests Complete!"
echo "============================================================"
echo -e "${NC}"

