"""
Hospital Multi-Agent System - Local Version
Runs entirely locally with Bedrock API calls
"""

import json
import os
from datetime import datetime
from typing import Dict, Any
import boto3

# Load mock patient data
def load_mock_data():
    """Load mock patient data from JSON"""
    with open('data/mock_patients.json', 'r') as f:
        return {p['patient_id']: p for p in json.load(f)}

# Initialize
PATIENTS = load_mock_data()
APPOINTMENTS = {}
MEMORY = {}

# Initialize Bedrock client
bedrock_runtime = boto3.client('bedrock-runtime', region_name='us-east-1')

def call_claude(prompt: str) -> str:
    """Call Claude via Bedrock"""
    try:
        response = bedrock_runtime.invoke_model(
            modelId='anthropic.claude-3-5-sonnet-20240620-v1:0',
            body=json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 2000,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            })
        )
        
        result = json.loads(response['body'].read())
        return result['content'][0]['text']
    except Exception as e:
        print(f"Bedrock API Error: {e}")
        return f"Error calling Claude: {str(e)}"

def get_patient_context(patient_id: str) -> Dict[str, Any]:
    """Get patient context"""
    patient = PATIENTS.get(patient_id, {})
    return {
        'medical_history': patient.get('medical_history', {}),
        'appointments': list(APPOINTMENTS.values()) if APPOINTMENTS else [],
        'recent_interactions': MEMORY.get(patient_id, [])
    }

def handle_query(prompt: str, patient_id: str) -> str:
    """Handle user query"""
    
    # Get patient context
    context = get_patient_context(patient_id)
    patient = PATIENTS.get(patient_id, {})
    
    # Determine which agent to use
    prompt_lower = prompt.lower()
    
    if any(word in prompt_lower for word in ['symptom', 'fever', 'cough', 'pain', 'sick', 'hurt']):
        agent_type = 'triage'
        system_prompt = f"""You are a hospital triage agent. Analyze symptoms and provide recommendations.

Patient Info:
- Name: {patient.get('name', 'Unknown')}
- Allergies: {', '.join(context['medical_history'].get('allergies', []))}
- Conditions: {', '.join(context['medical_history'].get('conditions', []))}

Analyze the symptoms and provide:
1. Urgency level (Low/Medium/High/Emergency)
2. Recommendations
3. Next steps

User Query: {prompt}"""
    
    elif any(word in prompt_lower for word in ['appointment', 'book', 'schedule', 'availability']):
        agent_type = 'booking'
        system_prompt = f"""You are a hospital booking agent. Help with appointment scheduling.

Patient Info:
- Name: {patient.get('name', 'Unknown')}
- Recent Appointments: {len(context['appointments'])}

Provide available slots and help book appointments.

User Query: {prompt}"""
    
    elif any(word in prompt_lower for word in ['remind', 'notification', 'follow-up']):
        agent_type = 'reminder'
        system_prompt = f"""You are a hospital reminder agent. Manage notifications and follow-ups.

Patient Info:
- Name: {patient.get('name', 'Unknown')}
- Upcoming: {len(context['appointments'])} appointments

User Query: {prompt}"""
    
    else:
        agent_type = 'general'
        system_prompt = f"""You are a helpful hospital AI assistant. You can help with:
- Symptom triage and health concerns
- Appointment booking and scheduling  
- Reminders and follow-ups

Patient: {patient.get('name', 'Unknown')}

User Query: {prompt}"""
    
    # Call Claude via Bedrock
    print(f"\n🤖 Routing to: {agent_type.upper()} Agent")
    print(f"📞 Calling Claude via Bedrock...")
    
    response = call_claude(system_prompt)
    
    # Store in memory
    if patient_id not in MEMORY:
        MEMORY[patient_id] = []
    MEMORY[patient_id].append({
        'query': prompt,
        'response': response[:200],  # Store truncated
        'agent': agent_type,
        'timestamp': datetime.now().isoformat()
    })
    
    return response

def main():
    """Main CLI interface"""
    print("\n" + "="*60)
    print("🏥 Hospital Multi-Agent System - Local Mode")
    print("="*60)
    print("\nAvailable Patients:")
    for pid, patient in PATIENTS.items():
        print(f"  {pid}: {patient['name']}")
    print("\n" + "="*60)
    
    while True:
        print("\n")
        patient_id = input("Enter Patient ID (or 'quit'): ").strip()
        
        if patient_id.lower() == 'quit':
            print("\n👋 Goodbye!")
            break
        
        if patient_id not in PATIENTS:
            print(f"❌ Patient {patient_id} not found. Try: P12345")
            continue
        
        patient = PATIENTS[patient_id]
        print(f"\n✅ Selected: {patient['name']} ({patient_id})")
        
        while True:
            print("\n" + "-"*60)
            query = input("Your question (or 'back'): ").strip()
            
            if query.lower() == 'back':
                break
            
            if not query:
                continue
            
            # Process query
            response = handle_query(query, patient_id)
            
            print("\n" + "="*60)
            print("🤖 AI Assistant Response:")
            print("="*60)
            print(response)
            print("="*60)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


