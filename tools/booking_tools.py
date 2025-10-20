"""
Booking Agent Tools
Functions for appointment scheduling and management
"""

import os
import json
import uuid
from typing import Dict, Any, List
from datetime import datetime, timedelta

import boto3
from botocore.exceptions import ClientError


# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb', region_name=os.getenv('AWS_REGION', 'us-east-1'))


def check_availability(department: str, date: str, doctor_name: str = None) -> Dict[str, Any]:
    """
    Check available appointment slots
    
    Args:
        department: Department name (e.g., "Pediatrics", "General Medicine")
        date: Date in YYYY-MM-DD format
        doctor_name: Optional specific doctor name
    
    Returns:
        Dictionary with available slots
    """
    # For MVP, generate mock availability
    # In production, this would query a real scheduling system
    
    try:
        target_date = datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        return {
            "error": "Invalid date format. Use YYYY-MM-DD",
            "available_slots": []
        }
    
    # Generate available slots (9 AM to 5 PM, every 30 min)
    slots = []
    start_hour = 9
    end_hour = 17
    
    for hour in range(start_hour, end_hour):
        for minute in [0, 30]:
            slot_time = f"{hour:02d}:{minute:02d}"
            slots.append({
                "time": slot_time,
                "doctor": doctor_name or _get_available_doctor(department),
                "department": department,
                "available": True
            })
    
    return {
        "date": date,
        "department": department,
        "available_slots": slots[:10],  # Return first 10 slots for MVP
        "total_available": len(slots)
    }


def book_appointment(patient_id: str, department: str, date: str, 
                    time: str, reason: str) -> Dict[str, Any]:
    """
    Book an appointment for a patient
    
    Args:
        patient_id: Patient identifier
        department: Department name
        date: Date in YYYY-MM-DD format
        time: Time in HH:MM format
        reason: Reason for visit
    
    Returns:
        Dictionary with booking confirmation
    """
    try:
        table = dynamodb.Table(os.getenv('APPOINTMENTS_TABLE', 'hospital-appointments'))
        
        appointment_id = str(uuid.uuid4())
        appointment = {
            'appointment_id': appointment_id,
            'patient_id': patient_id,
            'department': department,
            'date': date,
            'time': time,
            'reason': reason,
            'doctor': _get_available_doctor(department),
            'status': 'confirmed',
            'created_at': datetime.utcnow().isoformat(),
            'reminder_sent': False
        }
        
        # Store in DynamoDB
        table.put_item(Item=appointment)
        
        return {
            "status": "success",
            "appointment_id": appointment_id,
            "confirmation": f"Appointment confirmed for {date} at {time}",
            "department": department,
            "doctor": appointment['doctor'],
            "instructions": "Please arrive 15 minutes early. Bring insurance card and ID."
        }
        
    except ClientError as e:
        print(f"Error booking appointment: {e}")
        return {
            "status": "failed",
            "error": "Unable to book appointment. Please try again."
        }


def get_appointments(patient_id: str, status: str = "all") -> Dict[str, Any]:
    """
    Retrieve patient appointments
    
    Args:
        patient_id: Patient identifier
        status: Filter by status (confirmed, cancelled, completed, all)
    
    Returns:
        Dictionary with list of appointments
    """
    try:
        table = dynamodb.Table(os.getenv('APPOINTMENTS_TABLE', 'hospital-appointments'))
        
        # Query appointments for patient
        response = table.query(
            IndexName='PatientIndex',  # Assuming GSI exists
            KeyConditionExpression='patient_id = :pid',
            ExpressionAttributeValues={':pid': patient_id}
        )
        
        appointments = response.get('Items', [])
        
        # Filter by status if specified
        if status != "all":
            appointments = [apt for apt in appointments if apt.get('status') == status]
        
        # Sort by date
        appointments.sort(key=lambda x: f"{x.get('date', '')} {x.get('time', '')}", reverse=True)
        
        return {
            "patient_id": patient_id,
            "appointments": appointments,
            "total": len(appointments)
        }
        
    except ClientError as e:
        print(f"Error retrieving appointments: {e}")
        # Return mock data for MVP if DynamoDB fails
        return {
            "patient_id": patient_id,
            "appointments": [],
            "total": 0,
            "note": "Using mock data - DynamoDB not yet configured"
        }


def cancel_appointment(appointment_id: str, reason: str = "") -> Dict[str, Any]:
    """
    Cancel an appointment
    
    Args:
        appointment_id: Appointment identifier
        reason: Optional cancellation reason
    
    Returns:
        Cancellation confirmation
    """
    try:
        table = dynamodb.Table(os.getenv('APPOINTMENTS_TABLE', 'hospital-appointments'))
        
        # Update appointment status
        response = table.update_item(
            Key={'appointment_id': appointment_id},
            UpdateExpression='SET #status = :status, cancellation_reason = :reason, cancelled_at = :time',
            ExpressionAttributeNames={'#status': 'status'},
            ExpressionAttributeValues={
                ':status': 'cancelled',
                ':reason': reason,
                ':time': datetime.utcnow().isoformat()
            },
            ReturnValues='ALL_NEW'
        )
        
        return {
            "status": "success",
            "message": "Appointment cancelled successfully",
            "appointment_id": appointment_id
        }
        
    except ClientError as e:
        print(f"Error cancelling appointment: {e}")
        return {
            "status": "failed",
            "error": "Unable to cancel appointment"
        }


def _get_available_doctor(department: str) -> str:
    """Get available doctor for department (mock for MVP)"""
    doctors = {
        "Pediatrics": "Dr. Sarah Johnson",
        "General Medicine": "Dr. Michael Chen",
        "Cardiology": "Dr. Emily Rodriguez",
        "Emergency": "Dr. James Wilson",
        "Orthopedics": "Dr. Lisa Anderson"
    }
    return doctors.get(department, "Dr. Available Physician")

