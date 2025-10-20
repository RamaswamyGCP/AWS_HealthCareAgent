"""
Triage Agent Tools
Functions for symptom analysis and patient history retrieval
"""

import os
import json
from typing import Dict, Any, List
from datetime import datetime

import boto3
from botocore.exceptions import ClientError


# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb', region_name=os.getenv('AWS_REGION', 'us-east-1'))


def search_symptoms(patient_id: str, symptoms: List[str]) -> Dict[str, Any]:
    """
    Analyze symptoms and provide triage recommendation
    
    Args:
        patient_id: Patient identifier
        symptoms: List of symptoms
    
    Returns:
        Dictionary with urgency level and recommendations
    """
    # Symptom urgency mapping (simplified for MVP)
    high_risk_keywords = ['chest pain', 'difficulty breathing', 'severe bleeding', 
                          'unconscious', 'seizure', 'stroke', 'heart attack']
    medium_risk_keywords = ['fever', 'vomiting', 'severe pain', 'injury', 'infection']
    
    symptoms_lower = [s.lower() for s in symptoms]
    
    # Determine urgency
    urgency = "Low"
    for symptom in symptoms_lower:
        if any(keyword in symptom for keyword in high_risk_keywords):
            urgency = "Emergency"
            break
        elif any(keyword in symptom for keyword in medium_risk_keywords):
            urgency = "Medium"
    
    # Get patient history for additional context
    patient_history = _get_patient_medical_history(patient_id)
    
    # Generate recommendation
    if urgency == "Emergency":
        recommendation = "Seek immediate emergency care. Call 911 or go to nearest ER."
        next_steps = ["Go to Emergency Room immediately", "Call 911 if unable to transport"]
    elif urgency == "Medium":
        recommendation = "Schedule appointment with doctor within 24-48 hours."
        next_steps = ["Book appointment with primary care", "Monitor symptoms", "Seek ER if worsens"]
    else:
        recommendation = "Monitor symptoms. Home care may be sufficient."
        next_steps = ["Rest and hydrate", "Over-the-counter medication if needed", 
                     "Call if symptoms worsen or persist beyond 3 days"]
    
    return {
        "urgency": urgency,
        "recommendation": recommendation,
        "next_steps": next_steps,
        "relevant_history": patient_history.get('conditions', []),
        "allergies": patient_history.get('allergies', []),
        "timestamp": datetime.utcnow().isoformat()
    }


def get_patient_history(patient_id: str) -> Dict[str, Any]:
    """
    Retrieve patient medical history from DynamoDB
    
    Args:
        patient_id: Patient identifier
    
    Returns:
        Dictionary with patient medical history
    """
    return _get_patient_medical_history(patient_id)


def _get_patient_medical_history(patient_id: str) -> Dict[str, Any]:
    """Internal function to fetch patient history from DynamoDB"""
    try:
        table = dynamodb.Table(os.getenv('PATIENTS_TABLE', 'hospital-patients'))
        response = table.get_item(Key={'patient_id': patient_id})
        
        if 'Item' in response:
            patient = response['Item']
            return {
                'conditions': patient.get('medical_history', {}).get('conditions', []),
                'allergies': patient.get('medical_history', {}).get('allergies', []),
                'medications': patient.get('medical_history', {}).get('medications', []),
                'last_visit': patient.get('last_visit', 'N/A')
            }
        else:
            return {
                'conditions': [],
                'allergies': [],
                'medications': [],
                'last_visit': 'No previous visits'
            }
    
    except ClientError as e:
        print(f"Error retrieving patient history: {e}")
        return {
            'conditions': [],
            'allergies': [],
            'medications': [],
            'last_visit': 'Error retrieving history'
        }


def assess_urgency_with_history(symptoms: List[str], medical_history: Dict[str, Any]) -> str:
    """
    Assess urgency considering patient medical history
    
    Args:
        symptoms: List of symptoms
        medical_history: Patient medical history
    
    Returns:
        Urgency level: Emergency, High, Medium, or Low
    """
    urgency_score = 0
    
    # Base score from symptoms
    high_risk_symptoms = ['chest pain', 'difficulty breathing', 'severe bleeding']
    medium_risk_symptoms = ['fever', 'vomiting', 'severe pain']
    
    for symptom in symptoms:
        symptom_lower = symptom.lower()
        if any(hrs in symptom_lower for hrs in high_risk_symptoms):
            urgency_score += 3
        elif any(mrs in symptom_lower for mrs in medium_risk_symptoms):
            urgency_score += 2
        else:
            urgency_score += 1
    
    # Adjust based on history
    high_risk_conditions = ['diabetes', 'heart disease', 'asthma', 'copd', 'immunocompromised']
    patient_conditions = [c.lower() for c in medical_history.get('conditions', [])]
    
    if any(hrc in pc for hrc in high_risk_conditions for pc in patient_conditions):
        urgency_score += 1
    
    # Determine final urgency
    if urgency_score >= 4:
        return "Emergency"
    elif urgency_score >= 3:
        return "High"
    elif urgency_score >= 2:
        return "Medium"
    else:
        return "Low"

