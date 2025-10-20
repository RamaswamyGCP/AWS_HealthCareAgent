"""
Load mock FHIR-like data into DynamoDB
Run this script to populate test data for the hackathon demo
"""

import json
import os
import boto3
from botocore.exceptions import ClientError
from datetime import datetime, timedelta


def load_patients(table_name: str, data_file: str = 'mock_patients.json'):
    """Load patient data into DynamoDB"""
    dynamodb = boto3.resource('dynamodb', region_name=os.getenv('AWS_REGION', 'us-east-1'))
    table = dynamodb.Table(table_name)
    
    # Load mock data
    with open(data_file, 'r') as f:
        patients = json.load(f)
    
    # Insert patients
    for patient in patients:
        try:
            table.put_item(Item=patient)
            print(f"✓ Loaded patient: {patient['name']} ({patient['patient_id']})")
        except ClientError as e:
            print(f"✗ Error loading patient {patient['patient_id']}: {e}")
    
    print(f"\nTotal patients loaded: {len(patients)}")


def create_sample_appointments(table_name: str):
    """Create sample appointments for demo"""
    dynamodb = boto3.resource('dynamodb', region_name=os.getenv('AWS_REGION', 'us-east-1'))
    table = dynamodb.Table(table_name)
    
    # Sample appointments
    appointments = [
        {
            'appointment_id': 'APT-001',
            'patient_id': 'P12345',
            'department': 'Pediatrics',
            'date': (datetime.now() + timedelta(days=2)).strftime('%Y-%m-%d'),
            'time': '10:00',
            'reason': 'Asthma checkup',
            'doctor': 'Dr. Sarah Johnson',
            'status': 'confirmed',
            'created_at': datetime.utcnow().isoformat(),
            'reminder_sent': False
        },
        {
            'appointment_id': 'APT-002',
            'patient_id': 'P12346',
            'department': 'General Medicine',
            'date': (datetime.now() + timedelta(days=5)).strftime('%Y-%m-%d'),
            'time': '14:30',
            'reason': 'Diabetes follow-up',
            'doctor': 'Dr. Michael Chen',
            'status': 'confirmed',
            'created_at': datetime.utcnow().isoformat(),
            'reminder_sent': False
        },
        {
            'appointment_id': 'APT-003',
            'patient_id': 'P12348',
            'department': 'Cardiology',
            'date': (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d'),
            'time': '09:00',
            'reason': 'Heart checkup',
            'doctor': 'Dr. Emily Rodriguez',
            'status': 'confirmed',
            'created_at': datetime.utcnow().isoformat(),
            'reminder_sent': False
        }
    ]
    
    for appointment in appointments:
        try:
            table.put_item(Item=appointment)
            print(f"✓ Created appointment: {appointment['appointment_id']} for {appointment['patient_id']}")
        except ClientError as e:
            print(f"✗ Error creating appointment {appointment['appointment_id']}: {e}")
    
    print(f"\nTotal appointments created: {len(appointments)}")


def initialize_memory_table(table_name: str):
    """Initialize memory table with sample data"""
    dynamodb = boto3.resource('dynamodb', region_name=os.getenv('AWS_REGION', 'us-east-1'))
    table = dynamodb.Table(table_name)
    
    # Sample memory entries
    memories = [
        {
            'memory_id': 'MEM-001',
            'patient_id': 'P12345',
            'memory_type': 'interaction',
            'content': 'Patient called about fever and cough. Recommended monitoring.',
            'timestamp': (datetime.now() - timedelta(days=3)).isoformat()
        },
        {
            'memory_id': 'MEM-002',
            'patient_id': 'P12346',
            'memory_type': 'interaction',
            'content': 'Patient requested prescription refill for Metformin.',
            'timestamp': (datetime.now() - timedelta(days=1)).isoformat()
        }
    ]
    
    for memory in memories:
        try:
            table.put_item(Item=memory)
            print(f"✓ Created memory entry: {memory['memory_id']}")
        except ClientError as e:
            print(f"✗ Error creating memory {memory['memory_id']}: {e}")
    
    print(f"\nTotal memory entries created: {len(memories)}")


if __name__ == '__main__':
    import sys
    
    print("=" * 60)
    print("Hospital Multi-Agent System - Data Loader")
    print("=" * 60)
    print()
    
    # Get table names from environment or use defaults
    patients_table = os.getenv('PATIENTS_TABLE', 'hospital-patients')
    appointments_table = os.getenv('APPOINTMENTS_TABLE', 'hospital-appointments')
    memory_table = os.getenv('MEMORY_TABLE', 'hospital-memory')
    
    print(f"Target Tables:")
    print(f"  - Patients: {patients_table}")
    print(f"  - Appointments: {appointments_table}")
    print(f"  - Memory: {memory_table}")
    print()
    
    try:
        # Load patients
        print("Loading patient data...")
        load_patients(patients_table)
        print()
        
        # Create appointments
        print("Creating sample appointments...")
        create_sample_appointments(appointments_table)
        print()
        
        # Initialize memory
        print("Initializing memory table...")
        initialize_memory_table(memory_table)
        print()
        
        print("=" * 60)
        print("✓ Data loading complete!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n✗ Error during data loading: {e}")
        sys.exit(1)

