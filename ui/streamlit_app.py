"""
Hospital Multi-Agent System - Streamlit UI
Demo interface for the hackathon
"""

import streamlit as st
import requests
import json
import os
from datetime import datetime
import time
import sys
sys.path.insert(0, '/Users/ramaswamy/Documents/AWSOpenHack/hospital-multi-agent')

# Import local agent for direct Bedrock integration
try:
    from local_agent import handle_query, PATIENTS
    BEDROCK_AVAILABLE = True
except ImportError:
    BEDROCK_AVAILABLE = False


# Page config
st.set_page_config(
    page_title="Hospital AI Assistant",
    page_icon="🏥",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Ultra Clean, Modern Healthcare UI
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    /* Main App Background - Pure White */
    .stApp {
        background-color: #ffffff;
        background-image: 
            radial-gradient(at 0% 0%, rgba(59, 130, 246, 0.03) 0px, transparent 50%),
            radial-gradient(at 100% 100%, rgba(147, 51, 234, 0.03) 0px, transparent 50%);
    }
    
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main Header */
    .main-header {
        font-size: 1.75rem;
        font-weight: 700;
        color: #0f172a;
        text-align: center;
        margin: 0.5rem 0 0.5rem 0;
        letter-spacing: -0.02em;
    }
    
    /* Info Banner - Clean Card */
    .stAlert {
        background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
        color: white;
        border: none;
        border-radius: 16px;
        padding: 1rem 1.5rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        margin-bottom: 2rem;
    }
    
    .stAlert > div {
        color: white !important;
    }
    
    /* User Message - Light Blue Bubble */
    .user-message {
        background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
        color: #1e40af;
        padding: 0.5rem 0.75rem;
        border-radius: 12px 12px 4px 12px;
        margin: 0.25rem 0;
        max-width: 75%;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(59, 130, 246, 0.2);
        font-size: 0.9rem;
    }
    
    .user-message strong {
        display: block;
        margin-bottom: 0.25rem;
        font-size: 0.75rem;
        font-weight: 600;
        color: #1e3a8a;
        opacity: 0.8;
    }
    
    /* AI Assistant Message - White Card */
    .assistant-message {
        background: #ffffff;
        color: #1e293b;
        padding: 0.75rem;
        border-radius: 12px 12px 12px 4px;
        margin: 0.25rem 0;
        max-width: 85%;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.06);
        border: 1px solid #e2e8f0;
        line-height: 1.5;
        font-size: 0.9rem;
    }
    
    .assistant-message strong:first-child {
        display: block;
        margin-bottom: 0.5rem;
        font-size: 0.85rem;
        font-weight: 600;
        color: #3b82f6;
    }
    
    /* Content Typography */
    .assistant-message p {
        margin-bottom: 0.4rem;
        color: #334155;
    }
    
    .assistant-message strong {
        color: #0f172a;
        font-weight: 600;
    }
    
    .assistant-message ul, .assistant-message ol {
        margin: 0.4rem 0 0.4rem 1.2rem;
        color: #475569;
    }
    
    .assistant-message li {
        margin-bottom: 0.25rem;
        line-height: 1.4;
    }
    
    /* Urgency Badges - Clean Pills */
    .urgency-high, .urgency-emergency {
        background: #fef2f2;
        color: #dc2626;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-weight: 600;
        font-size: 0.75rem;
        display: inline-block;
        border: 1px solid #fecaca;
        margin: 0.15rem 0;
    }
    
    .urgency-medium {
        background: #fffbeb;
        color: #d97706;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-weight: 600;
        font-size: 0.75rem;
        display: inline-block;
        border: 1px solid #fde68a;
        margin: 0.15rem 0;
    }
    
    .urgency-low {
        background: #f0fdf4;
        color: #16a34a;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-weight: 600;
        font-size: 0.75rem;
        display: inline-block;
        border: 1px solid #bbf7d0;
        margin: 0.15rem 0;
    }
    
    /* Sidebar - Compact with Scroll */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #E8F6F3 0%, #f8fafc 100%);
        border-right: 2px solid #5DADE2;
        overflow-y: auto !important;
        max-height: 100vh;
    }
    
    section[data-testid="stSidebar"] > div {
        padding-top: 0.25rem;
        padding-bottom: 0.5rem;
    }
    
    section[data-testid="stSidebar"] .block-container {
        padding-top: 0.25rem;
        padding-bottom: 0.25rem;
    }
    
    /* Hide sidebar scrollbar but keep functionality */
    section[data-testid="stSidebar"]::-webkit-scrollbar {
        width: 4px;
    }
    
    section[data-testid="stSidebar"]::-webkit-scrollbar-thumb {
        background: #5DADE2;
        border-radius: 2px;
    }
    
    section[data-testid="stSidebar"] .stMarkdown h3 {
        color: #2C3E50;
        font-weight: 700;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.35rem;
        margin-top: 0.5rem;
    }
    
    section[data-testid="stSidebar"] label {
        color: #2C3E50 !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
    }
    
    /* Sidebar selectbox - EXTREME force black text */
    section[data-testid="stSidebar"] .stSelectbox *,
    section[data-testid="stSidebar"] .stSelectbox *::before,
    section[data-testid="stSidebar"] .stSelectbox *::after {
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
        fill: #000000 !important;
        background-color: white !important;
        opacity: 1 !important;
    }
    
    section[data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] {
        background-color: white !important;
    }
    
    section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] span,
    section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] div {
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
    }
    
    /* Selectbox Styling - NUCLEAR OPTION - Force Black Text */
    .stSelectbox {
        margin-bottom: 0.5rem;
    }
    
    .stSelectbox label {
        color: #2C3E50 !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
    }
    
    /* Main selectbox container */
    .stSelectbox > div > div {
        background-color: white !important;
        border: 2px solid #5DADE2 !important;
        border-radius: 8px !important;
        box-shadow: 0 2px 4px rgba(93, 173, 226, 0.2) !important;
    }
    
    /* Selected value display - ALL POSSIBLE SELECTORS */
    .stSelectbox div[data-baseweb="select"],
    .stSelectbox div[data-baseweb="select"] *,
    .stSelectbox [data-baseweb="select"] [role="button"],
    .stSelectbox [data-baseweb="select"] [role="button"] *,
    .stSelectbox [data-baseweb="select"] [role="button"] > div,
    .stSelectbox [data-baseweb="select"] [role="button"] > div *,
    .stSelectbox [data-baseweb="select"] div,
    .stSelectbox [data-baseweb="select"] span {
        color: #000000 !important;
        background-color: white !important;
        -webkit-text-fill-color: #000000 !important;
        fill: #000000 !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        text-shadow: none !important;
        opacity: 1 !important;
    }
    
    /* Dropdown menu items */
    .stSelectbox div[role="listbox"] {
        background-color: white !important;
    }
    
    .stSelectbox div[role="listbox"] li,
    .stSelectbox div[role="listbox"] li * {
        color: #000000 !important;
        background-color: white !important;
        font-size: 0.95rem !important;
        -webkit-text-fill-color: #000000 !important;
    }
    
    .stSelectbox div[role="listbox"] li:hover {
        background-color: #E8F6F3 !important;
        color: #000000 !important;
    }
    
    /* Nuclear override - target ALL elements */
    .stSelectbox *,
    .stSelectbox *::before,
    .stSelectbox *::after {
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
    }
    
    /* Checkbox Styling */
    .stCheckbox {
        background: white;
        padding: 0.4rem;
        border-radius: 6px;
        border: 1px solid #e2e8f0;
        margin-bottom: 0.3rem;
    }
    
    .stCheckbox label {
        color: #0f172a !important;
        font-weight: 500;
        font-size: 0.75rem;
    }
    
    /* Metrics - Clean Cards */
    div[data-testid="stMetric"] {
        background: white;
        padding: 0.5rem;
        border-radius: 8px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.03);
    }
    
    div[data-testid="stMetricLabel"] {
        color: #64748b;
        font-weight: 500;
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    div[data-testid="stMetricValue"] {
        color: #3b82f6;
        font-weight: 700;
        font-size: 1.25rem;
    }
    
    /* Buttons - Adira Healthcare Style */
    .stButton button {
        background: white;
        color: #5DADE2;
        border: 1.5px solid #5DADE2;
        border-radius: 8px;
        padding: 0.5rem 0.75rem;
        font-weight: 600;
        font-size: 0.8rem;
        transition: all 0.2s ease;
        width: 100%;
        margin-bottom: 0.25rem;
    }
    
    .stButton button:hover {
        background: linear-gradient(135deg, #5DADE2 0%, #27AE60 100%);
        color: white;
        transform: translateY(-1px);
        box-shadow: 0 4px 6px -1px rgba(93, 173, 226, 0.4);
    }
    
    /* Chat Input - Highly Visible Text */
    .stChatInput {
        border-top: 2px solid #27AE60;
        padding-top: 1rem;
        margin-top: 0.5rem;
        background: linear-gradient(135deg, #E8F6F3 0%, #ffffff 100%) !important;
        padding-bottom: 1rem;
    }
    
    .stChatInput > div {
        border: 2px solid #5DADE2 !important;
        border-radius: 12px;
        background: white !important;
        box-shadow: 0 4px 12px rgba(93, 173, 226, 0.25);
    }
    
    .stChatInput > div:focus-within {
        border-color: #27AE60 !important;
        box-shadow: 0 4px 16px rgba(39, 174, 96, 0.3);
    }
    
    .stChatInput input {
        color: #000000 !important;
        font-size: 1rem !important;
        font-weight: 500 !important;
        background-color: white !important;
    }
    
    .stChatInput input::placeholder {
        color: #555555 !important;
        font-weight: 400 !important;
        opacity: 0.8 !important;
    }
    
    .stChatInput textarea {
        color: #000000 !important;
        font-size: 1rem !important;
        font-weight: 500 !important;
        background-color: white !important;
    }
    
    /* Override Streamlit's default input styling */
    div[data-baseweb="base-input"] {
        background-color: white !important;
    }
    
    div[data-baseweb="base-input"] input {
        color: #000000 !important;
        background-color: white !important;
    }
    
    div[data-baseweb="base-input"] textarea {
        color: #000000 !important;
        background-color: white !important;
    }
    
    /* Bottom chat section background */
    .stBottom {
        background: linear-gradient(135deg, #E8F6F3 0%, #ffffff 100%) !important;
    }
    
    /* Chat input specific overrides */
    [data-testid="stChatInput"] input,
    [data-testid="stChatInput"] textarea {
        color: #000000 !important;
        background: white !important;
        -webkit-text-fill-color: #000000 !important;
    }
    
    /* Sample Queries Cards */
    .sample-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        margin-bottom: 1rem;
        transition: all 0.2s ease;
    }
    
    .sample-card:hover {
        border-color: #3b82f6;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    /* Dividers */
    hr {
        border: none;
        border-top: 1px solid #e2e8f0;
        margin: 0.3rem 0;
    }
    
    /* Sidebar dividers */
    section[data-testid="stSidebar"] hr {
        margin: 0.4rem 0;
        border-color: #D6EAF8;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f5f9;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #cbd5e1;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #94a3b8;
    }
    
    /* Spinner - Adira Healthcare Style */
    .stSpinner > div {
        border-top-color: #5DADE2 !important;
        border-right-color: #27AE60 !important;
    }
    
    /* Spinner container */
    div[data-testid="stSpinner"] {
        text-align: center;
    }
    
    div[data-testid="stSpinner"] > div {
        color: #2C3E50 !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
    }
    
    /* Add pulse animation to spinner text */
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.6; }
    }
    
    div[data-testid="stSpinner"] {
        animation: pulse 1.5s ease-in-out infinite;
    }
</style>
""", unsafe_allow_html=True)


# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'patient_id' not in st.session_state:
    st.session_state.patient_id = "P12345"
if 'agent_stats' not in st.session_state:
    st.session_state.agent_stats = {
        'total_queries': 0,
        'triage_count': 0,
        'booking_count': 0,
        'reminder_count': 0
    }


def call_agent_api(prompt: str, patient_id: str, local_mode: bool = True):
    """Call the multi-agent system"""
    
    # NEW: Direct Bedrock integration for live AI responses
    if BEDROCK_AVAILABLE:
        try:
            print(f"🔥 Calling live Bedrock LLM for patient {patient_id}...")
            
            # Call the local_agent which uses Bedrock directly
            result = handle_query(prompt, patient_id)
            
            # Update stats based on query type
            st.session_state.agent_stats['total_queries'] += 1
            prompt_lower = prompt.lower()
            if any(word in prompt_lower for word in ['symptom', 'fever', 'cough', 'pain', 'sick']):
                st.session_state.agent_stats['triage_count'] += 1
            elif any(word in prompt_lower for word in ['appointment', 'book', 'schedule']):
                st.session_state.agent_stats['booking_count'] += 1
            elif any(word in prompt_lower for word in ['remind', 'notification']):
                st.session_state.agent_stats['reminder_count'] += 1
            
            return {
                "result": result,
                "patient_id": patient_id,
                "timestamp": datetime.utcnow().isoformat(),
                "status": "success",
                "bedrock": True
            }
        except Exception as e:
            print(f"❌ Bedrock error: {e}")
            # Fall back to mock on error
            return mock_agent_response(prompt, patient_id)
    
    # FALLBACK: Try server endpoint (for full deployment)
    if local_mode:
        endpoint = "http://localhost:8080/invocations"
    else:
        endpoint = os.getenv('API_GATEWAY_URL', 'http://localhost:8080/invocations')
    
    payload = {
        "prompt": prompt,
        "patient_id": patient_id
    }
    
    try:
        response = requests.post(
            endpoint,
            json=payload,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            return {
                "error": f"API returned status {response.status_code}",
                "status": "failed"
            }
    except requests.exceptions.ConnectionError:
        # Fallback to mock response for demo
        return mock_agent_response(prompt, patient_id)
    except Exception as e:
        return {
            "error": str(e),
            "status": "failed"
        }


def mock_agent_response(prompt: str, patient_id: str):
    """Mock response for demo when backend is not running"""
    prompt_lower = prompt.lower()
    
    if any(word in prompt_lower for word in ['symptom', 'fever', 'cough', 'pain', 'sick']):
        agent_type = 'triage'
        result = """Based on your symptoms, I recommend the following:

**Urgency Level:** Medium

**Recommendation:** Schedule an appointment with your doctor within 24-48 hours.

**Next Steps:**
1. Monitor your symptoms
2. Rest and stay hydrated
3. Take over-the-counter medication if needed
4. Seek emergency care if symptoms worsen

**Note:** I've checked your medical history and noted your allergies to Penicillin and Peanuts."""
    
    elif any(word in prompt_lower for word in ['appointment', 'book', 'schedule', 'availability']):
        agent_type = 'booking'
        result = """I can help you schedule an appointment!

**Available Slots:**
- October 12, 2025 at 10:00 AM - Dr. Sarah Johnson
- October 12, 2025 at 2:30 PM - Dr. Michael Chen
- October 13, 2025 at 9:00 AM - Dr. Emily Rodriguez

Would you like to book one of these slots? Please specify your preferred date and time."""
    
    elif any(word in prompt_lower for word in ['remind', 'notification', 'follow-up']):
        agent_type = 'reminder'
        result = """I've set up your reminders!

**Upcoming Reminders:**
1. Appointment reminder - October 12, 2025 at 8:00 AM
2. Medication refill - October 15, 2025
3. Follow-up checkup - October 30, 2025

You'll receive notifications via email 24 hours before each event."""
    
    else:
        agent_type = 'general'
        result = """Hello! I'm your hospital AI assistant. I can help you with:

- 🩺 **Symptom Analysis & Triage**: Assess your symptoms and recommend next steps
- 📅 **Appointment Booking**: Schedule appointments with available doctors
- 🔔 **Reminders & Follow-ups**: Set up notifications and manage follow-up care

How can I assist you today?"""
    
    # Update stats
    st.session_state.agent_stats['total_queries'] += 1
    if agent_type == 'triage':
        st.session_state.agent_stats['triage_count'] += 1
    elif agent_type == 'booking':
        st.session_state.agent_stats['booking_count'] += 1
    elif agent_type == 'reminder':
        st.session_state.agent_stats['reminder_count'] += 1
    
    return {
        "result": result,
        "patient_id": patient_id,
        "timestamp": datetime.utcnow().isoformat(),
        "status": "success",
        "agent_type": agent_type,
        "mock": True
    }


# Sidebar with clean design
with st.sidebar:
    # Adira Healthcare Logo
    st.markdown("""
    <div style="text-align: center; padding: 0.5rem 0 0.75rem 0;">
        <div style="
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 70px;
            height: 70px;
            border-radius: 50%;
            border: 3px solid #5DADE2;
            background: linear-gradient(135deg, #E8F6F3 0%, #D6EAF8 100%);
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin-bottom: 0.5rem;
        ">
            <span style="font-size: 2rem; color: #5DADE2;">A+</span>
        </div>
        <div style="margin-top: 0.25rem;">
            <div style="font-size: 1rem; font-weight: 700; color: #2C3E50; letter-spacing: 0.02em;">Adira <span style="color: #27AE60;">Healthcare</span></div>
            <div style="font-size: 0.65rem; color: #7F8C8D; margin-top: 0.1rem; font-style: italic;">Compassionate Care</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 👤 Patient Information")
    
    # Patient selector
    patients = {
        "P12345": "Emma Johnson (Pediatric)",
        "P12346": "Michael Chen (Diabetic)",
        "P12347": "Sarah Williams (Healthy)",
        "P12348": "David Martinez (Cardiac)",
        "P12349": "Olivia Brown (Pediatric)"
    }
    
    selected_patient = st.selectbox(
        "Select Patient",
        options=list(patients.keys()),
        format_func=lambda x: patients[x],
        index=0
    )
    st.session_state.patient_id = selected_patient
    
    # Set local_mode to True by default (hidden from UI)
    local_mode = True
    
    st.divider()
    
    # Statistics in a clean layout
    st.markdown("### 📊 Agent Statistics")
    
    # Two column layout for metrics
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Queries", st.session_state.agent_stats['total_queries'])
        st.metric("Triage", st.session_state.agent_stats['triage_count'])
    with col2:
        st.metric("Bookings", st.session_state.agent_stats['booking_count'])
        st.metric("Reminders", st.session_state.agent_stats['reminder_count'])
    
    st.divider()
    
    # Quick actions with better styling and visibility
    st.markdown("### ⚡ Quick Actions")
    
    # Use columns for more compact layout
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🩺 Symptoms", use_container_width=True, key="btn_symptoms"):
            st.session_state.quick_prompt = "I have fever and cough. What should I do?"
    
    with col2:
        if st.button("📅 Book", use_container_width=True, key="btn_book"):
            st.session_state.quick_prompt = "I'd like to schedule an appointment for next week"
    
    # Full width clear button
    if st.button("🔄 Clear Chat", use_container_width=True, key="btn_clear"):
        st.session_state.messages = []
        st.rerun()


# Main content area - Adira Healthcare Branding
st.markdown("""
<div style="text-align: center; padding: 0.25rem 0 0.5rem 0;">
    <h1 style="font-size: 1.5rem; font-weight: 700; color: #2C3E50; margin: 0; font-family: 'Inter', -apple-system, sans-serif;">
        🏥 Adira Healthcare AI Assistant
    </h1>
    <p style="color: #27AE60; font-size: 0.85rem; margin-top: 0.25rem; font-weight: 500;">
        Compassionate AI-powered care • AWS Bedrock
    </p>
</div>
""", unsafe_allow_html=True)

# Patient info card - Adira Healthcare colors (Production)
st.markdown(f"""
<div style="background: linear-gradient(135deg, #5DADE2 0%, #27AE60 100%); color: white; padding: 0.5rem 1rem; border-radius: 8px; text-align: center; margin-bottom: 0.5rem; font-size: 0.85rem; box-shadow: 0 3px 8px rgba(93, 173, 226, 0.3);">
    <strong>Current Patient:</strong> {patients[st.session_state.patient_id]}
</div>
""", unsafe_allow_html=True)

# Chat container
chat_container = st.container()

with chat_container:
    # Display chat messages with clean inline styling
    for message in st.session_state.messages:
        role = message['role']
        content = message['content']
        
        if role == 'user':
            # User message - right aligned, light blue
            cols = st.columns([1, 3])
            with cols[1]:
                st.markdown(f'''
                <div style="background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%); 
                            color: #1e40af; 
                            padding: 0.5rem 0.75rem; 
                            border-radius: 12px 12px 4px 12px; 
                            margin: 0.25rem 0;
                            border: 1px solid rgba(59, 130, 246, 0.2);
                            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.08);
                            font-size: 0.9rem;">
                    <div style="font-size: 0.75rem; font-weight: 600; color: #1e3a8a; margin-bottom: 0.25rem;">
                        👤 You
                    </div>
                    <div style="color: #1e40af;">{content}</div>
                </div>
                ''', unsafe_allow_html=True)
        else:
            # AI message - left aligned, white
            cols = st.columns([3, 1])
            with cols[0]:
                # Format content with proper styling
                formatted_content = content
                
                # Replace urgency levels with styled badges
                if "**Urgency Level:** Medium" in formatted_content:
                    formatted_content = formatted_content.replace(
                        "**Urgency Level:** Medium",
                        '<strong>Urgency Level:</strong> <span style="background: #fffbeb; color: #d97706; padding: 0.25rem 0.75rem; border-radius: 9999px; font-weight: 600; font-size: 0.875rem; border: 1px solid #fde68a;">Medium</span>'
                    )
                if "**Urgency Level:** High" in formatted_content:
                    formatted_content = formatted_content.replace(
                        "**Urgency Level:** High",
                        '<strong>Urgency Level:</strong> <span style="background: #fef2f2; color: #dc2626; padding: 0.25rem 0.75rem; border-radius: 9999px; font-weight: 600; font-size: 0.875rem; border: 1px solid #fecaca;">High</span>'
                    )
                if "**Urgency Level:** Low" in formatted_content:
                    formatted_content = formatted_content.replace(
                        "**Urgency Level:** Low",
                        '<strong>Urgency Level:</strong> <span style="background: #f0fdf4; color: #16a34a; padding: 0.25rem 0.75rem; border-radius: 9999px; font-weight: 600; font-size: 0.875rem; border: 1px solid #bbf7d0;">Low</span>'
                    )
                
                # Convert markdown bold to HTML
                formatted_content = formatted_content.replace("**", "<strong>").replace("**", "</strong>")
                
                st.markdown(f'''
                <div style="background: #ffffff; 
                            color: #1e293b; 
                            padding: 0.75rem; 
                            border-radius: 12px 12px 12px 4px; 
                            margin: 0.25rem 0;
                            border: 1px solid #e2e8f0;
                            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
                            font-size: 0.9rem;">
                    <div style="font-size: 0.85rem; font-weight: 600; color: #3b82f6; margin-bottom: 0.5rem;">
                        🤖 AI Assistant
                    </div>
                    <div style="color: #334155; line-height: 1.5;">{formatted_content}</div>
                </div>
                ''', unsafe_allow_html=True)

# Chat input
user_input = st.chat_input("Ask me about symptoms, appointments, or reminders...")

# Handle quick prompts
if 'quick_prompt' in st.session_state:
    user_input = st.session_state.quick_prompt
    del st.session_state.quick_prompt

# Process user input
if user_input:
    # Add user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input,
        "timestamp": datetime.now()
    })
    
    # Show professional loading indicator
    with st.spinner("🏥 Adira Healthcare AI is analyzing..."):
        # Call agent API
        response = call_agent_api(user_input, st.session_state.patient_id, local_mode)
        
        # Simulate processing time
        time.sleep(1)
    
    # Add assistant response
    if response.get('status') == 'success':
        assistant_message = response.get('result', 'No response')
        
        # Add appropriate note based on source (Production - cleaner messages)
        if response.get('bedrock'):
            assistant_message += "\n\n---\n✅ *Powered by AWS Bedrock (Claude 3.5 Sonnet)*"
        elif response.get('mock'):
            assistant_message += "\n\n---\n*Note: Using offline mode.*"
        
        st.session_state.messages.append({
            "role": "assistant",
            "content": assistant_message,
            "timestamp": datetime.now()
        })
    else:
        error_message = f"❌ Error: {response.get('error', 'Unknown error')}"
        st.session_state.messages.append({
            "role": "assistant",
            "content": error_message,
            "timestamp": datetime.now()
        })
    
    st.rerun()

# Compact sample queries section - only shown when no messages
if len(st.session_state.messages) == 0:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #E8F6F3 0%, #D6EAF8 100%); padding: 0.75rem 1rem; border-radius: 8px; border: 2px solid #5DADE2; margin: 0.5rem 0;">
        <div style="font-size: 0.75rem; font-weight: 600; color: #2C3E50; margin-bottom: 0.4rem;">💡 Try asking:</div>
        <div style="font-size: 0.8rem; color: #34495E; line-height: 1.4;">
            • "My child has fever and cough" • "Book appointment for next week" • "Show my upcoming reminders"
        </div>
    </div>
    """, unsafe_allow_html=True)

# Compact footer with Adira Healthcare branding (Production)
st.markdown("""
<div style='text-align: center; padding: 0.75rem 0; margin-top: 0.5rem; border-top: 1px solid #E8F6F3;'>
    <p style='color: #7F8C8D; margin: 0; font-size: 0.75rem;'>
        Adira Healthcare • Powered by AWS Bedrock
    </p>
</div>
""", unsafe_allow_html=True)

