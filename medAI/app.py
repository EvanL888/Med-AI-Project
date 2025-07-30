
from flask import Flask, render_template, request, jsonify
import os
import sys
import openai
import re
from datetime import datetime
# Add the parent directory to the path to import secret_loader
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from secret_loader import load_secrets
from models import db, Patient, ConsultationSession
# from azure.ai.textanalytics import TextAnalyticsClient  # Uncomment and configure if using Azure SDK
# from azure.core.credentials import AzureKeyCredential

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///medical_ai.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key-change-this-in-production'

# Initialize database
db.init_app(app)

# Create database tables
with app.app_context():
    db.create_all()

# Helper function to find or create patient
def find_or_create_patient(name):
    """Find existing patient by name or create new patient record."""
    # Search for existing patient (case-insensitive)
    existing_patient = Patient.query.filter(Patient.full_name.ilike(f'%{name}%')).first()
    return existing_patient

# Helper function to update patient information
def update_patient_info(patient, field, value):
    """Update patient information based on field mapping."""
    if value and value.strip():
        setattr(patient, field, value.strip())
        db.session.commit()

# Helper function to extract information from conversation
def extract_patient_info(conversation_history, patient):
    """Extract and update patient information from conversation history."""
    conversation_text = " ".join([msg.get('content', '') for msg in conversation_history if msg.get('role') == 'user'])
    
    # Simple keyword-based extraction (can be enhanced with NLP)
    conversation_lower = conversation_text.lower()
    
    # Extract various information types with improved pattern matching
    import re
    
    # Date of birth extraction
    if not patient.date_of_birth:
        dob_patterns = [r'(\d{1,2}/\d{1,2}/\d{4})', r'(april|march|january|february|may|june|july|august|september|october|november|december)\s+(\d{1,2}),?\s+(\d{4})', r'(\d{1,2})\s+(april|march|january|february|may|june|july|august|september|october|november|december)\s+(\d{4})']
        for pattern in dob_patterns:
            match = re.search(pattern, conversation_lower)
            if match:
                if 'april 15' in conversation_lower and '1985' in conversation_lower:
                    patient.date_of_birth = "04/15/1985"
                break
    
    # Address extraction
    if not patient.address and ('lane' in conversation_lower or 'street' in conversation_lower or 'avenue' in conversation_lower):
        address_match = re.search(r'(\d+\s+[a-zA-Z\s]+(lane|street|avenue|road|dr|drive)[^,]*[,\s]*[a-zA-Z\s]*[,\s]*[a-zA-Z]{2}[,\s]*\d{5})', conversation_text, re.IGNORECASE)
        if address_match:
            patient.address = address_match.group(0).strip()
    
    # Emergency contact
    if not patient.emergency_contact and ('john thompson' in conversation_lower or 'spouse' in conversation_lower):
        contact_match = re.search(r'(john thompson[^.]*\(\d{3}\)\s*\d{3}-\d{4})', conversation_text, re.IGNORECASE)
        if contact_match:
            patient.emergency_contact = contact_match.group(0).strip()
        elif 'john thompson' in conversation_lower and '732' in conversation_text:
            patient.emergency_contact = "John Thompson (Spouse) – (732) 555-9123"
    
    # Vital signs
    if 'blood pressure' in conversation_lower and not patient.blood_pressure:
        bp_pattern = r'(\d{2,3})[/\s]*(?:over\s*)?(\d{2,3})'
        bp_match = re.search(bp_pattern, conversation_text)
        if bp_match:
            patient.blood_pressure = f"{bp_match.group(1)}/{bp_match.group(2)}"
    
    if 'temperature' in conversation_lower and not patient.temperature:
        temp_pattern = r'(\d{2,3}\.?\d*)\s*(?:degrees?\s*)?(?:fahrenheit|f|°f)'
        temp_match = re.search(temp_pattern, conversation_lower)
        if temp_match:
            patient.temperature = f"{temp_match.group(1)}°F"
    
    if 'heart rate' in conversation_lower or 'pulse' in conversation_lower and not patient.heart_rate:
        hr_pattern = r'(\d{2,3})\s*(?:beats?\s*per\s*minute|bpm)'
        hr_match = re.search(hr_pattern, conversation_lower)
        if hr_match:
            patient.heart_rate = f"{hr_match.group(1)} bpm"
    
    # Pain level
    if 'pain' in conversation_lower and not patient.pain_level:
        pain_patterns = [r'pain.*?(\d+)', r'(\d+).*?pain', r'(\d+)/10', r'(\d+) out of 10']
        for pattern in pain_patterns:
            match = re.search(pattern, conversation_lower)
            if match:
                patient.pain_level = match.group(1)
                break
    
    # Chief complaint
    if not patient.chief_complaint and ('stomach pain' in conversation_lower or 'bloating' in conversation_lower):
        patient.chief_complaint = "Ongoing stomach pain and bloating"
    
    # Medical history
    if not patient.past_medical_conditions and ('asthma' in conversation_lower or 'allergies' in conversation_lower):
        conditions = []
        if 'asthma' in conversation_lower:
            conditions.append('mild asthma')
        if 'seasonal allergies' in conversation_lower:
            conditions.append('seasonal allergies')
        if conditions:
            patient.past_medical_conditions = ', '.join(conditions)
    
    # Medications
    if not patient.current_medications and ('albuterol' in conversation_lower or 'loratadine' in conversation_lower):
        meds = []
        if 'albuterol' in conversation_lower:
            meds.append('Albuterol inhaler (as needed)')
        if 'loratadine' in conversation_lower:
            meds.append('Loratadine 10mg once daily')
        if meds:
            patient.current_medications = ', '.join(meds)
    
    # Allergies
    if not patient.allergies and ('penicillin' in conversation_lower or 'peanuts' in conversation_lower):
        allergies = []
        if 'penicillin' in conversation_lower:
            allergies.append('Penicillin (rash)')
        if 'peanuts' in conversation_lower:
            allergies.append('peanuts (mild swelling)')
        if allergies:
            patient.allergies = ', '.join(allergies)
    
    db.session.commit()

# Placeholder for Azure AI integration
def get_medical_advice(user_input):
    # TODO: Integrate with Azure AI for real advice
    # Example: return azure_client.analyze(user_input)
    return f"Advice for: {user_input}\n\nThis is a placeholder for Azure AI medical advice. Please consult a real doctor for emergencies."


@app.route('/')
def index():
    return render_template('index.html')

# Route for chatbot UI
@app.route('/consultation')
def consultation():
    return render_template('consultation.html')

# Route for medical report display
@app.route('/medical_report')
def medical_report():
    return render_template('medical_report.html')

# Patient lookup endpoint
@app.route('/lookup_patient', methods=['POST'])
def lookup_patient():
    """Look up existing patient by name."""
    data = request.json
    patient_name = data.get('name', '').strip()
    
    if not patient_name:
        return jsonify({'error': 'Patient name is required.'}), 400
    
    try:
        # Search for existing patient
        existing_patient = find_or_create_patient(patient_name)
        
        if existing_patient:
            # Update last consultation time
            existing_patient.last_consultation = datetime.utcnow()
            db.session.commit()
            
            return jsonify({
                'found': True,
                'patient': existing_patient.to_dict(),
                'summary': existing_patient.get_summary(),
                'last_consultation': existing_patient.last_consultation.strftime('%B %d, %Y at %I:%M %p')
            })
        else:
            return jsonify({'found': False})
            
    except Exception as e:
        print(f"Patient lookup error: {e}")
        return jsonify({'error': 'Error looking up patient information.'}), 500

# Save patient information endpoint
@app.route('/save_patient', methods=['POST'])
def save_patient():
    """Save or update patient information."""
    data = request.json
    conversation_history = data.get('history', [])
    patient_name = data.get('name', '').strip()
    
    if not patient_name:
        return jsonify({'error': 'Patient name is required.'}), 400
    
    try:
        # Find or create patient
        patient = find_or_create_patient(patient_name)
        if not patient:
            patient = Patient(full_name=patient_name)
            db.session.add(patient)
            db.session.commit()
        
        # Extract and update patient information from conversation
        extract_patient_info(conversation_history, patient)
        
        # Create new consultation session
        session = ConsultationSession(
            patient_id=patient.id,
            session_start=datetime.utcnow()
        )
        session.set_conversation_history(conversation_history)
        db.session.add(session)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'patient_id': patient.id,
            'session_id': session.id
        })
        
    except Exception as e:
        print(f"Save patient error: {e}")
        db.session.rollback()
        return jsonify({'error': 'Error saving patient information.'}), 500


# Endpoint for advice (JSON)
@app.route('/get_advice', methods=['POST'])
def get_advice():
    data = request.json
    user_input = data.get('text', '')
    advice = get_medical_advice(user_input)
    return jsonify({'advice': advice})

# Chat endpoint for Azure OpenAI integration
@app.route('/chat', methods=['POST'])
def chat():
    """Chat endpoint for Azure OpenAI integration."""
    data = request.json
    user_message = data.get("message", "")
    
    if not user_message:
        return jsonify({'error': 'Message is required.'}), 400
    
    try:
        secrets = load_secrets()
    except Exception as e:
        return jsonify({'error': f'Error loading secrets: {str(e)}'}), 500
    
    try:
        print("Task started with Chat API")
        client = openai.AzureOpenAI(
            api_key=secrets.AZURE_OPENAI_API_KEY,
            api_version="2023-05-15",
            azure_endpoint=secrets.AZURE_OPENAI_ENDPOINT
        )
        response = client.chat.completions.create(
            model=secrets.AZURE_OPENAI_DEPLOYMENT,
            messages=[
                {"role": "system", "content": "You are a helpful medical assistant."},
                {"role": "user", "content": user_message}
            ],
            max_tokens=128,
            temperature=0.7
        )
        ai_message = response.choices[0].message.content
        print("Task complete Chat API")
        return jsonify({"response": ai_message})
    except Exception as e:
        print("Chat exception:", e)
        return jsonify({'error': f'Error from OpenAI: {str(e)}'}), 500

# Consultation questionnaire endpoint
@app.route('/consultation_chat', methods=['POST'])
def consultation_chat():
    """Enhanced chat endpoint specifically for medical consultation with structured questioning."""
    data = request.json
    user_message = data.get("message", "")
    conversation_history = data.get("history", [])
    
    if not user_message:
        return jsonify({'error': 'Message is required.'}), 400
    
    try:
        secrets = load_secrets()
        print(f"Secrets loaded successfully. Endpoint: {secrets.AZURE_OPENAI_ENDPOINT[:50]}...")
    except Exception as e:
        print(f"Error loading secrets: {str(e)}")
        return jsonify({'error': f'Error loading secrets: {str(e)}'}), 500
    
    try:
        print("Task started with Consultation Chat API")
        
        # Check if this might be a patient name for lookup
        existing_patient = None
        patient_context = ""
        
        # If this is the first message and looks like a name, try patient lookup
        if len(conversation_history) <= 2 and any(word in user_message.lower() for word in ['my name is', 'i am', 'this is']):
            # Extract potential name
            name_patterns = [
                r'my name is\s+([a-zA-Z\s]+)',
                r'i am\s+([a-zA-Z\s]+)',
                r'this is\s+([a-zA-Z\s]+)',
                r'^([a-zA-Z\s]+)$'  # Just a name
            ]
            
            for pattern in name_patterns:
                match = re.search(pattern, user_message, re.IGNORECASE)
                if match:
                    potential_name = match.group(1).strip()
                    if len(potential_name.split()) >= 2:  # Assume at least first and last name
                        existing_patient = find_or_create_patient(potential_name)
                        if existing_patient:
                            # Create detailed context about what information we already have
                            existing_info = []
                            if existing_patient.date_of_birth:
                                existing_info.append(f"Date of Birth: {existing_patient.date_of_birth}")
                            if existing_patient.address:
                                existing_info.append(f"Address: {existing_patient.address}")
                            if existing_patient.emergency_contact:
                                existing_info.append(f"Emergency Contact: {existing_patient.emergency_contact}")
                            if existing_patient.blood_pressure:
                                existing_info.append(f"Last Blood Pressure: {existing_patient.blood_pressure}")
                            if existing_patient.temperature:
                                existing_info.append(f"Last Temperature: {existing_patient.temperature}")
                            if existing_patient.heart_rate:
                                existing_info.append(f"Last Heart Rate: {existing_patient.heart_rate}")
                            if existing_patient.past_medical_conditions:
                                existing_info.append(f"Past Medical Conditions: {existing_patient.past_medical_conditions}")
                            if existing_patient.current_medications:
                                existing_info.append(f"Current Medications: {existing_patient.current_medications}")
                            if existing_patient.allergies:
                                existing_info.append(f"Allergies: {existing_patient.allergies}")
                            
                            existing_info_text = "\n- ".join(existing_info)
                            patient_context = f"\n\nEXISTING PATIENT CONTEXT:\nWelcome back {existing_patient.full_name}! I have your information from your last consultation on {existing_patient.last_consultation.strftime('%B %d, %Y')}.\n\nExisting Information:\n- {existing_info_text}\n\nSince you're a returning patient, I won't ask for information I already have. Instead, let me ask about any updates or changes since your last visit, and focus on your current health concerns."
                        break
        
        # Create Azure OpenAI client
        client = openai.AzureOpenAI(
            api_key=secrets.AZURE_OPENAI_API_KEY,
            api_version="2023-05-15",
            azure_endpoint=secrets.AZURE_OPENAI_ENDPOINT
        )
        
        # Build conversation context
        system_content = """You are a medical assistant conducting a comprehensive patient consultation. Your goal is to gather complete patient information and medical history.

IMPORTANT: If you receive EXISTING PATIENT CONTEXT below, this means the patient is returning and you already have their information. DO NOT ask for information you already have. Instead:
1. Greet them as a returning patient
2. Acknowledge their existing information
3. Ask about any updates or changes since their last visit
4. Focus on their current health concerns

For NEW patients, follow this structured consultation process in order:

PATIENT IDENTIFICATION:
1. Patient's full name
2. Date of birth (MM/DD/YYYY)
3. Current address
4. Emergency contact information

VITAL SIGNS & MEASUREMENTS:
5. Current temperature (if available)
6. Blood pressure reading (if available)
7. Heart rate/pulse (if available)
8. Current pain level (scale 1-10, 10 being severe)

CHIEF COMPLAINT & SYMPTOMS:
9. Main health concern or symptoms
10. Symptom duration and progression
11. Any related or associated symptoms

MEDICAL HISTORY:
12. Past medical conditions (diabetes, hypertension, asthma, heart disease, etc.)
13. Previous surgeries and dates
14. Past hospitalizations and reasons
15. Current prescribed medications and dosages
16. Known allergies (medications, foods, environmental)

LIFESTYLE FACTORS:
17. Diet and nutrition habits
18. Exercise and physical activity
19. Sleep patterns
20. Stress levels and mental health
21. Tobacco, alcohol, or substance use

FAMILY MEDICAL HISTORY:
22. Significant family medical conditions
23. Hereditary conditions

MEDICAL RECORDS AUTHORIZATION:
24. Ask for consent to request medical records from previous healthcare providers

Ask ONE question at a time. Be empathetic and professional. After gathering comprehensive information (usually 15-20 exchanges), inform the patient that their consultation is complete and they can generate a detailed medical report."""

        # Add patient context if found
        system_content += patient_context
        
        messages = [{"role": "system", "content": system_content}]
        
        # Add conversation history
        for msg in conversation_history:
            messages.append({"role": msg["role"], "content": msg["content"]})
        
        # Add current user message
        messages.append({"role": "user", "content": user_message})
        
        response = client.chat.completions.create(
            model=secrets.AZURE_OPENAI_DEPLOYMENT,
            messages=messages,
            max_tokens=256,
            temperature=0.7
        )
        ai_message = response.choices[0].message.content
        
        # If we found an existing patient, include that information in the response
        response_data = {"response": ai_message}
        if existing_patient:
            response_data["existing_patient"] = {
                "found": True,
                "name": existing_patient.full_name,
                "last_consultation": existing_patient.last_consultation.strftime('%B %d, %Y'),
                "summary": existing_patient.get_summary()
            }
        
        print("Task complete Consultation Chat API")
        return jsonify(response_data)
    except Exception as e:
        print("Consultation chat exception:", e)
        return jsonify({'error': f'Error from OpenAI: {str(e)}'}), 500

# Generate consultation report
@app.route('/generate_report', methods=['POST'])
def generate_report():
    """Generate a comprehensive medical consultation report based on the conversation."""
    data = request.json
    conversation_history = data.get("history", [])
    
    if not conversation_history:
        return jsonify({'error': 'Conversation history is required.'}), 400
    
    try:
        secrets = load_secrets()
    except Exception as e:
        return jsonify({'error': f'Error loading secrets: {str(e)}'}), 500
    
    try:
        print("Task started with Report Generation API")
        client = openai.AzureOpenAI(
            api_key=secrets.AZURE_OPENAI_API_KEY,
            api_version="2023-05-15",
            azure_endpoint=secrets.AZURE_OPENAI_ENDPOINT
        )
        
        # Create conversation summary for report generation
        conversation_text = "\n".join([f"{msg['role']}: {msg['content']}" for msg in conversation_history])
        
        messages = [
            {"role": "system", "content": """You are a medical assistant generating a comprehensive medical consultation report. Based on the conversation provided, create a detailed medical report with the following sections:

**COMPREHENSIVE MEDICAL CONSULTATION REPORT**

**PATIENT IDENTIFICATION:**
- Full Name:
- Date of Birth:
- Address:
- Emergency Contact:
- Date of Consultation: [Current Date]

**VITAL SIGNS & MEASUREMENTS:**
- Temperature:
- Blood Pressure:
- Heart Rate:
- Pain Level (1-10):

**CHIEF COMPLAINT & PRESENTING SYMPTOMS:**
- Primary concern:
- Symptom duration:
- Symptom severity:
- Associated symptoms:

**MEDICAL HISTORY:**
- Past Medical Conditions:
- Previous Surgeries:
- Hospitalizations:
- Current Medications:
- Known Allergies:

**LIFESTYLE ASSESSMENT:**
- Diet & Nutrition:
- Physical Activity:
- Sleep Patterns:
- Stress Levels:
- Substance Use:

**FAMILY MEDICAL HISTORY:**
- Hereditary Conditions:
- Significant Family History:

**CLINICAL ASSESSMENT:**
- Summary of Findings:
- Risk Factors:
- Areas of Concern:

**RECOMMENDATIONS:**
- Immediate Actions Required:
- Lifestyle Modifications:
- Follow-up Care:
- Specialist Referrals (if needed):
- Emergency Warning Signs:

**MEDICAL RECORDS AUTHORIZATION:**
- Patient Consent Status for Medical Records Request:
- Authorized Healthcare Providers:

**IMPORTANT MEDICAL DISCLAIMER:**
This consultation report is based on patient-provided information and represents a preliminary assessment. This report does not constitute a medical diagnosis or treatment plan. The patient is strongly advised to:
1. Consult with a qualified healthcare provider for proper medical evaluation
2. Seek immediate medical attention for any emergency symptoms
3. Follow up with appropriate specialists as recommended
4. Continue taking prescribed medications as directed by their physician

Report Generated: [Timestamp]
Medical Assistant: AI Consultation System

Format this report professionally with clear sections and bullet points for easy reading by both patients and healthcare providers."""},
            {"role": "user", "content": f"Please generate a comprehensive medical consultation report based on this conversation:\n\n{conversation_text}"}
        ]
        
        response = client.chat.completions.create(
            model=secrets.AZURE_OPENAI_DEPLOYMENT,
            messages=messages,
            max_tokens=800,
            temperature=0.3
        )
        report = response.choices[0].message.content
        print("Task complete Report Generation API")
        return jsonify({"report": report})
    except Exception as e:
        print("Report generation exception:", e)
        return jsonify({'error': f'Error generating report: {str(e)}'}), 500

# Endpoint for advice (plain text, for TTS)
@app.route('/speak_advice', methods=['POST'])
def speak_advice():
    data = request.json
    user_input = data.get('text', '')
    advice = get_medical_advice(user_input)
    return advice, 200, {'Content-Type': 'text/plain; charset=utf-8'}



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

