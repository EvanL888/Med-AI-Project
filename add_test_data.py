#!/usr/bin/env python3
"""
Script to add test patient data to the medical AI database.
This will populate the database with Sarah Thompson's comprehensive medical information.
"""

import os
import sys
from datetime import datetime

# Add the current directory to the path to import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'medAI'))

from medAI.app import app
from medAI.models import db, Patient, ConsultationSession

def add_sarah_thompson_data():
    """Add Sarah Thompson's comprehensive medical data to the database."""
    
    with app.app_context():
        # Check if patient already exists
        existing_patient = Patient.query.filter_by(full_name="Sarah Thompson").first()
        if existing_patient:
            print("Sarah Thompson already exists in the database. Updating her information...")
            patient = existing_patient
        else:
            print("Creating new patient record for Sarah Thompson...")
            patient = Patient()
        
        # PATIENT IDENTIFICATION
        patient.full_name = "Sarah Thompson"
        patient.date_of_birth = datetime.strptime("04/15/1985", "%m/%d/%Y").date()
        patient.address = "127 Maplewood Lane, Edison, NJ 08820"
        patient.emergency_contact = "John Thompson (Spouse) – (732) 555-9123"
        
        # VITAL SIGNS & MEASUREMENTS
        patient.temperature = "98.6°F"
        patient.blood_pressure = "128/82 mmHg"
        patient.heart_rate = "78 bpm"
        patient.pain_level = "4"  # 4/10 mild abdominal discomfort
        
        # CHIEF COMPLAINT & SYMPTOMS
        patient.chief_complaint = "Ongoing stomach pain and bloating"
        patient.symptom_duration = "Started mildly 5 days ago, gradually worsening"
        patient.associated_symptoms = "Occasional nausea, loss of appetite, and fatigue"
        
        # MEDICAL HISTORY
        patient.past_conditions = "Mild asthma, seasonal allergies"
        patient.surgeries = "Appendectomy (2010)"
        patient.hospitalizations = "Hospitalized for dehydration (2015)"
        patient.current_medications = "Albuterol inhaler (as needed), Loratadine 10mg once daily"
        patient.allergies = "Penicillin (rash), peanuts (mild swelling)"
        
        # LIFESTYLE FACTORS
        patient.diet_habits = "Balanced diet, avoids processed foods, drinks 1 coffee/day"
        patient.exercise_habits = "Walks 30 minutes daily, yoga twice a week"
        patient.sleep_patterns = "Typically 6-7 hours/night, difficulty falling asleep"
        patient.stress_levels = "Moderate work-related stress, occasional anxiety"
        patient.substance_use = "Non-smoker, drinks wine socially (1-2x/month), no drug use"
        
        # FAMILY MEDICAL HISTORY
        patient.family_history = "Mother: Type 2 diabetes, hypothyroidism; Father: Hypertension, high cholesterol"
        patient.hereditary_conditions = "None reported"
        
        # MEDICAL RECORDS AUTHORIZATION
        patient.records_authorization = "Patient consents to request medical records from previous healthcare providers (Dr. Elaine Harper, Primary Care – Edison Medical Group)"
        
        # Set consultation timestamp
        patient.last_consultation = datetime.utcnow()
        
        # Add to database
        if not existing_patient:
            db.session.add(patient)
        
        # Create a consultation session record
        session = ConsultationSession(
            patient_id=patient.id if existing_patient else None,
            session_start=datetime.utcnow(),
            session_end=datetime.utcnow()
        )
        
        # Create sample conversation history for the consultation
        conversation_history = [
            {"role": "assistant", "content": "Hello! I'm your medical assistant. Could you please tell me your full name?"},
            {"role": "user", "content": "My name is Sarah Thompson"},
            {"role": "assistant", "content": "Thank you, Sarah. What is your date of birth?"},
            {"role": "user", "content": "April 15th, 1985"},
            {"role": "assistant", "content": "What is your current address?"},
            {"role": "user", "content": "127 Maplewood Lane, Edison, NJ 08820"},
            {"role": "assistant", "content": "Could you provide emergency contact information?"},
            {"role": "user", "content": "John Thompson, my spouse, at (732) 555-9123"},
            {"role": "assistant", "content": "What is your current temperature if you've taken it?"},
            {"role": "user", "content": "98.6 degrees Fahrenheit"},
            {"role": "assistant", "content": "Do you have a recent blood pressure reading?"},
            {"role": "user", "content": "128 over 82"},
            {"role": "assistant", "content": "What about your heart rate or pulse?"},
            {"role": "user", "content": "78 beats per minute"},
            {"role": "assistant", "content": "On a scale of 1-10, what is your current pain level?"},
            {"role": "user", "content": "About a 4, I have mild abdominal discomfort"},
            {"role": "assistant", "content": "What is your main health concern today?"},
            {"role": "user", "content": "I've been having ongoing stomach pain and bloating"},
            {"role": "assistant", "content": "How long have you been experiencing these symptoms?"},
            {"role": "user", "content": "It started mildly about 5 days ago and has been gradually worsening"},
            {"role": "assistant", "content": "Are there any other related symptoms?"},
            {"role": "user", "content": "Yes, I've had occasional nausea, loss of appetite, and fatigue"},
            {"role": "assistant", "content": "Do you have any past medical conditions?"},
            {"role": "user", "content": "I have mild asthma and seasonal allergies"},
            {"role": "assistant", "content": "Have you had any surgeries?"},
            {"role": "user", "content": "Yes, I had an appendectomy in 2010"},
            {"role": "assistant", "content": "Any past hospitalizations?"},
            {"role": "user", "content": "I was hospitalized for dehydration in 2015"},
            {"role": "assistant", "content": "What medications are you currently taking?"},
            {"role": "user", "content": "I use an Albuterol inhaler as needed and take Loratadine 10mg once daily"},
            {"role": "assistant", "content": "Do you have any known allergies?"},
            {"role": "user", "content": "I'm allergic to Penicillin which gives me a rash, and peanuts cause mild swelling"},
            {"role": "assistant", "content": "Could you describe your diet and nutrition habits?"},
            {"role": "user", "content": "I eat a balanced diet, avoid processed foods, and drink about one coffee per day"},
            {"role": "assistant", "content": "What about exercise and physical activity?"},
            {"role": "user", "content": "I walk 30 minutes daily and do yoga twice a week"},
            {"role": "assistant", "content": "How are your sleep patterns?"},
            {"role": "user", "content": "I typically get 6-7 hours per night, but I have difficulty falling asleep"},
            {"role": "assistant", "content": "How would you describe your stress levels and mental health?"},
            {"role": "user", "content": "I have moderate work-related stress and occasional anxiety"},
            {"role": "assistant", "content": "Do you use tobacco, alcohol, or any substances?"},
            {"role": "user", "content": "I don't smoke, I drink wine socially maybe 1-2 times per month, and no drug use"},
            {"role": "assistant", "content": "Is there any significant family medical history?"},
            {"role": "user", "content": "My mother has Type 2 diabetes and hypothyroidism. My father has hypertension and high cholesterol"},
            {"role": "assistant", "content": "Any hereditary conditions we should know about?"},
            {"role": "user", "content": "None that I'm aware of"},
            {"role": "assistant", "content": "Finally, do you consent to us requesting medical records from your previous healthcare providers?"},
            {"role": "user", "content": "Yes, you can request records from Dr. Elaine Harper at Edison Medical Group"},
            {"role": "assistant", "content": "Thank you for providing all this comprehensive information, Sarah. Your consultation is now complete and I can generate a detailed medical report for you."}
        ]
        
        session.set_conversation_history(conversation_history)
        db.session.add(session)
        
        # Commit all changes
        db.session.commit()
        
        # Update the session with the patient ID after commit
        if not existing_patient:
            session.patient_id = patient.id
            db.session.commit()
        
        print(f"✅ Successfully added/updated Sarah Thompson's medical data!")
        print(f"   Patient ID: {patient.id}")
        print(f"   Session ID: {session.id}")
        print(f"   Last Consultation: {patient.last_consultation}")
        print(f"   Total conversation exchanges: {len(conversation_history)}")
        
        return patient, session

def main():
    """Main function to run the test data addition."""
    print("🏥 Adding comprehensive test data to Medical AI Database...")
    print("=" * 60)
    
    try:
        patient, session = add_sarah_thompson_data()
        print("\n" + "=" * 60)
        print("✅ Test data addition completed successfully!")
        print(f"\nPatient Summary:")
        print(f"Name: {patient.full_name}")
        print(f"DOB: {patient.date_of_birth}")
        print(f"Chief Complaint: {patient.chief_complaint}")
        print(f"Pain Level: {patient.pain_level}/10")
        print(f"Last Consultation: {patient.last_consultation}")
        
        print(f"\nYou can now test the patient lookup by:")
        print(f"1. Starting the Flask app")
        print(f"2. Going to the consultation page")
        print(f"3. Entering 'Sarah Thompson' as the patient name")
        print(f"4. The system should recognize her and load her existing data")
        
    except Exception as e:
        print(f"❌ Error adding test data: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
