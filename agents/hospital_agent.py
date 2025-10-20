"""
Hospital Multi-Agent System
Uses Bedrock AgentCore Runtime + Strands Agents for patient triage and care coordination
"""

import os
import json
import yaml
from typing import Dict, Any, List
from datetime import datetime

from bedrock_agentcore import BedrockAgentCoreApp
from strands import Agent
import boto3
from botocore.exceptions import ClientError


class HospitalMultiAgentSystem:
    """Multi-agent system for hospital patient management"""
    
    def __init__(self, config_path: str = "config.yaml"):
        """Initialize the multi-agent system"""
        self.app = BedrockAgentCoreApp()
        self.config = self._load_config(config_path)
        
        # Initialize AWS clients
        self.dynamodb = boto3.resource('dynamodb', region_name=os.getenv('AWS_REGION', 'us-east-1'))
        self.bedrock_runtime = boto3.client('bedrock-runtime', region_name=os.getenv('AWS_REGION', 'us-east-1'))
        
        # Initialize agents
        self.supervisor_agent = self._create_supervisor()
        self.triage_agent = self._create_triage_agent()
        self.booking_agent = self._create_booking_agent()
        self.reminder_agent = self._create_reminder_agent()
        
        # Memory store (in-memory for MVP, can be replaced with Bedrock Memory)
        self.session_memory = {}
        
    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from YAML file"""
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    
    def _create_supervisor(self) -> Agent:
        """Create supervisor agent for routing"""
        config = self.config['agents']['supervisor']
        
        agent = Agent(
            name=config['name'],
            instruction=config['instruction'],
            model=config['model_id']
        )
        
        return agent
    
    def _create_triage_agent(self) -> Agent:
        """Create triage agent for symptom analysis"""
        config = self.config['agents']['triage']
        
        # Register tools
        from tools.triage_tools import search_symptoms, get_patient_history
        
        agent = Agent(
            name=config['name'],
            instruction=config['instruction'],
            model=config['model_id'],
            tools=[search_symptoms, get_patient_history]
        )
        
        return agent
    
    def _create_booking_agent(self) -> Agent:
        """Create booking agent for appointments"""
        config = self.config['agents']['booking']
        
        # Register tools
        from tools.booking_tools import check_availability, book_appointment, get_appointments
        
        agent = Agent(
            name=config['name'],
            instruction=config['instruction'],
            model=config['model_id'],
            tools=[check_availability, book_appointment, get_appointments]
        )
        
        return agent
    
    def _create_reminder_agent(self) -> Agent:
        """Create reminder agent for notifications"""
        config = self.config['agents']['reminder']
        
        # Register tools
        from tools.reminder_tools import send_notification, schedule_reminder
        
        agent = Agent(
            name=config['name'],
            instruction=config['instruction'],
            model=config['model_id'],
            tools=[send_notification, schedule_reminder]
        )
        
        return agent
    
    def route_query(self, user_message: str, patient_id: str) -> str:
        """Route user query to appropriate agent"""
        
        # Step 1: Get patient context from memory
        context = self._get_patient_context(patient_id)
        
        # Step 2: Use supervisor to determine routing
        supervisor_prompt = f"""
        Patient ID: {patient_id}
        Patient Context: {json.dumps(context, indent=2)}
        
        User Query: {user_message}
        
        Analyze the query and determine which agent should handle it:
        - TriageAgent: For symptoms, medical concerns, urgency assessment
        - BookingAgent: For appointments, scheduling, availability
        - ReminderAgent: For follow-ups, notifications, reminders
        
        Respond with ONLY the agent name: TriageAgent, BookingAgent, or ReminderAgent
        """
        
        routing_result = self.supervisor_agent(supervisor_prompt)
        agent_name = routing_result.message.strip()
        
        # Step 3: Route to appropriate agent
        if "Triage" in agent_name:
            return self._handle_triage(user_message, patient_id, context)
        elif "Booking" in agent_name:
            return self._handle_booking(user_message, patient_id, context)
        elif "Reminder" in agent_name:
            return self._handle_reminder(user_message, patient_id, context)
        else:
            return "I'm not sure how to help with that. Please rephrase your question."
    
    def _handle_triage(self, message: str, patient_id: str, context: Dict) -> str:
        """Handle triage query"""
        triage_prompt = f"""
        Patient ID: {patient_id}
        Medical History: {json.dumps(context.get('medical_history', {}), indent=2)}
        
        Patient Query: {message}
        
        Analyze symptoms and provide triage recommendation.
        """
        
        result = self.triage_agent(triage_prompt)
        
        # Store in memory
        self._update_memory(patient_id, 'triage', result.message)
        
        return result.message
    
    def _handle_booking(self, message: str, patient_id: str, context: Dict) -> str:
        """Handle booking query"""
        booking_prompt = f"""
        Patient ID: {patient_id}
        Past Appointments: {json.dumps(context.get('appointments', []), indent=2)}
        
        Patient Query: {message}
        
        Help the patient with appointment scheduling.
        """
        
        result = self.booking_agent(booking_prompt)
        
        # Store in memory
        self._update_memory(patient_id, 'booking', result.message)
        
        return result.message
    
    def _handle_reminder(self, message: str, patient_id: str, context: Dict) -> str:
        """Handle reminder query"""
        reminder_prompt = f"""
        Patient ID: {patient_id}
        Upcoming Reminders: {json.dumps(context.get('reminders', []), indent=2)}
        
        Patient Query: {message}
        
        Help manage reminders and follow-ups.
        """
        
        result = self.reminder_agent(reminder_prompt)
        
        # Store in memory
        self._update_memory(patient_id, 'reminder', result.message)
        
        return result.message
    
    def _get_patient_context(self, patient_id: str) -> Dict:
        """Retrieve patient context from DynamoDB and memory"""
        context = {
            'medical_history': {},
            'appointments': [],
            'reminders': [],
            'recent_interactions': []
        }
        
        try:
            # Get from DynamoDB
            patients_table = self.dynamodb.Table(os.getenv('PATIENTS_TABLE', 'hospital-patients'))
            response = patients_table.get_item(Key={'patient_id': patient_id})
            
            if 'Item' in response:
                patient_data = response['Item']
                context['medical_history'] = patient_data.get('medical_history', {})
            
            # Get recent appointments
            appointments_table = self.dynamodb.Table(os.getenv('APPOINTMENTS_TABLE', 'hospital-appointments'))
            response = appointments_table.query(
                KeyConditionExpression='patient_id = :pid',
                ExpressionAttributeValues={':pid': patient_id},
                Limit=5
            )
            context['appointments'] = response.get('Items', [])
            
        except ClientError as e:
            print(f"Error retrieving patient context: {e}")
        
        # Get from session memory
        if patient_id in self.session_memory:
            context['recent_interactions'] = self.session_memory[patient_id]
        
        return context
    
    def _update_memory(self, patient_id: str, interaction_type: str, content: str):
        """Update session memory"""
        if patient_id not in self.session_memory:
            self.session_memory[patient_id] = []
        
        self.session_memory[patient_id].append({
            'type': interaction_type,
            'content': content,
            'timestamp': datetime.utcnow().isoformat()
        })
        
        # Keep only last 10 interactions per patient
        self.session_memory[patient_id] = self.session_memory[patient_id][-10:]


# Create app instance
hospital_system = HospitalMultiAgentSystem()
app = hospital_system.app


@app.entrypoint
def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Main entrypoint for the multi-agent system
    
    Expected payload:
    {
        "prompt": "My child has fever and cough",
        "patient_id": "P12345"
    }
    """
    try:
        user_message = payload.get("prompt", "")
        patient_id = payload.get("patient_id", "UNKNOWN")
        
        if not user_message:
            return {
                "error": "No prompt provided",
                "status": "failed"
            }
        
        # Route and process query
        response = hospital_system.route_query(user_message, patient_id)
        
        return {
            "result": response,
            "patient_id": patient_id,
            "timestamp": datetime.utcnow().isoformat(),
            "status": "success"
        }
        
    except Exception as e:
        return {
            "error": str(e),
            "status": "failed"
        }


if __name__ == "__main__":
    # Run locally for testing
    app.run()

