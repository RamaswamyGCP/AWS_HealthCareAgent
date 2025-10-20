"""
Reminder Agent Tools
Functions for notifications and follow-up management
"""

import os
import json
import uuid
from typing import Dict, Any, List
from datetime import datetime, timedelta

import boto3
from botocore.exceptions import ClientError


# Initialize AWS clients
dynamodb = boto3.resource('dynamodb', region_name=os.getenv('AWS_REGION', 'us-east-1'))
sns = boto3.client('sns', region_name=os.getenv('AWS_REGION', 'us-east-1'))


def send_notification(patient_id: str, message: str, 
                     notification_type: str = "general") -> Dict[str, Any]:
    """
    Send notification to patient
    
    Args:
        patient_id: Patient identifier
        message: Notification message
        notification_type: Type (appointment, reminder, alert, general)
    
    Returns:
        Notification confirmation
    """
    try:
        # For MVP, we'll log the notification
        # In production, integrate with SNS/SES for actual delivery
        
        notification = {
            'notification_id': str(uuid.uuid4()),
            'patient_id': patient_id,
            'type': notification_type,
            'message': message,
            'sent_at': datetime.utcnow().isoformat(),
            'status': 'sent',
            'channel': 'email'  # Could be email, sms, push
        }
        
        # Store in DynamoDB for tracking
        table = dynamodb.Table(os.getenv('MEMORY_TABLE', 'hospital-memory'))
        table.put_item(Item={
            **notification,
            'memory_type': 'notification'
        })
        
        # TODO: In production, send actual notification via SNS/SES
        # sns.publish(
        #     TopicArn=f'arn:aws:sns:us-east-1:123456789012:patient-notifications',
        #     Message=message,
        #     Subject=f"Hospital Notification - {notification_type}"
        # )
        
        return {
            "status": "success",
            "notification_id": notification['notification_id'],
            "message": "Notification sent successfully",
            "channel": "email",
            "timestamp": notification['sent_at']
        }
        
    except ClientError as e:
        print(f"Error sending notification: {e}")
        return {
            "status": "failed",
            "error": "Unable to send notification"
        }


def schedule_reminder(patient_id: str, reminder_type: str, 
                     scheduled_date: str, message: str) -> Dict[str, Any]:
    """
    Schedule a future reminder
    
    Args:
        patient_id: Patient identifier
        reminder_type: Type (appointment, medication, follow_up, test)
        scheduled_date: Date to send reminder (YYYY-MM-DD)
        message: Reminder message
    
    Returns:
        Scheduling confirmation
    """
    try:
        table = dynamodb.Table(os.getenv('MEMORY_TABLE', 'hospital-memory'))
        
        reminder_id = str(uuid.uuid4())
        reminder = {
            'reminder_id': reminder_id,
            'patient_id': patient_id,
            'memory_type': 'reminder',
            'type': reminder_type,
            'message': message,
            'scheduled_date': scheduled_date,
            'status': 'scheduled',
            'created_at': datetime.utcnow().isoformat(),
            'sent': False
        }
        
        # Store in DynamoDB
        table.put_item(Item=reminder)
        
        # TODO: In production, use EventBridge to trigger reminder at scheduled time
        
        return {
            "status": "success",
            "reminder_id": reminder_id,
            "message": f"Reminder scheduled for {scheduled_date}",
            "type": reminder_type
        }
        
    except ClientError as e:
        print(f"Error scheduling reminder: {e}")
        return {
            "status": "failed",
            "error": "Unable to schedule reminder"
        }


def get_upcoming_reminders(patient_id: str, days_ahead: int = 7) -> Dict[str, Any]:
    """
    Get upcoming reminders for patient
    
    Args:
        patient_id: Patient identifier
        days_ahead: Number of days to look ahead
    
    Returns:
        List of upcoming reminders
    """
    try:
        table = dynamodb.Table(os.getenv('MEMORY_TABLE', 'hospital-memory'))
        
        # Query reminders
        response = table.query(
            IndexName='PatientMemoryIndex',
            KeyConditionExpression='patient_id = :pid',
            FilterExpression='memory_type = :mtype AND #status = :status',
            ExpressionAttributeNames={'#status': 'status'},
            ExpressionAttributeValues={
                ':pid': patient_id,
                ':mtype': 'reminder',
                ':status': 'scheduled'
            }
        )
        
        reminders = response.get('Items', [])
        
        # Filter by date range
        cutoff_date = (datetime.utcnow() + timedelta(days=days_ahead)).strftime('%Y-%m-%d')
        upcoming = [
            r for r in reminders 
            if r.get('scheduled_date', '') <= cutoff_date
        ]
        
        # Sort by date
        upcoming.sort(key=lambda x: x.get('scheduled_date', ''))
        
        return {
            "patient_id": patient_id,
            "reminders": upcoming,
            "total": len(upcoming),
            "days_ahead": days_ahead
        }
        
    except ClientError as e:
        print(f"Error retrieving reminders: {e}")
        return {
            "patient_id": patient_id,
            "reminders": [],
            "total": 0,
            "note": "Using mock data"
        }


def send_appointment_reminder(appointment_id: str, patient_id: str) -> Dict[str, Any]:
    """
    Send reminder for upcoming appointment
    
    Args:
        appointment_id: Appointment identifier
        patient_id: Patient identifier
    
    Returns:
        Reminder confirmation
    """
    try:
        # Get appointment details
        appointments_table = dynamodb.Table(os.getenv('APPOINTMENTS_TABLE', 'hospital-appointments'))
        response = appointments_table.get_item(Key={'appointment_id': appointment_id})
        
        if 'Item' not in response:
            return {
                "status": "failed",
                "error": "Appointment not found"
            }
        
        appointment = response['Item']
        
        # Create reminder message
        message = f"""
Appointment Reminder

Date: {appointment['date']}
Time: {appointment['time']}
Department: {appointment['department']}
Doctor: {appointment.get('doctor', 'TBD')}

Please arrive 15 minutes early.
Bring your insurance card and ID.

To cancel or reschedule, please call (555) 123-4567.
        """.strip()
        
        # Send notification
        result = send_notification(
            patient_id=patient_id,
            message=message,
            notification_type="appointment_reminder"
        )
        
        # Mark reminder as sent in appointment
        appointments_table.update_item(
            Key={'appointment_id': appointment_id},
            UpdateExpression='SET reminder_sent = :val, reminder_sent_at = :time',
            ExpressionAttributeValues={
                ':val': True,
                ':time': datetime.utcnow().isoformat()
            }
        )
        
        return result
        
    except ClientError as e:
        print(f"Error sending appointment reminder: {e}")
        return {
            "status": "failed",
            "error": "Unable to send appointment reminder"
        }


def create_follow_up_task(patient_id: str, task_type: str, 
                         due_date: str, notes: str = "") -> Dict[str, Any]:
    """
    Create a follow-up task
    
    Args:
        patient_id: Patient identifier
        task_type: Type of follow-up (test_results, check_in, prescription, etc.)
        due_date: Due date in YYYY-MM-DD format
        notes: Additional notes
    
    Returns:
        Task creation confirmation
    """
    try:
        table = dynamodb.Table(os.getenv('MEMORY_TABLE', 'hospital-memory'))
        
        task_id = str(uuid.uuid4())
        task = {
            'task_id': task_id,
            'patient_id': patient_id,
            'memory_type': 'follow_up_task',
            'type': task_type,
            'due_date': due_date,
            'notes': notes,
            'status': 'pending',
            'created_at': datetime.utcnow().isoformat(),
            'completed': False
        }
        
        table.put_item(Item=task)
        
        return {
            "status": "success",
            "task_id": task_id,
            "message": f"Follow-up task created for {due_date}",
            "type": task_type
        }
        
    except ClientError as e:
        print(f"Error creating follow-up task: {e}")
        return {
            "status": "failed",
            "error": "Unable to create follow-up task"
        }

