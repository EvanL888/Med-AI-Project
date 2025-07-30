"""Database models for the medical AI consultation system."""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class Patient(db.Model):
    """Patient information model for storing comprehensive medical data."""
    id = db.Column(db.Integer, primary_key=True)
    
    # Patient Identification
    full_name = db.Column(db.String(200), nullable=False, index=True)
    date_of_birth = db.Column(db.String(20), nullable=True)
    address = db.Column(db.Text, nullable=True)
    emergency_contact = db.Column(db.Text, nullable=True)
    
    # Vital Signs & Measurements
    temperature = db.Column(db.String(50), nullable=True)
    blood_pressure = db.Column(db.String(50), nullable=True)
    heart_rate = db.Column(db.String(50), nullable=True)
    pain_level = db.Column(db.String(10), nullable=True)
    
    # Chief Complaint & Symptoms
    chief_complaint = db.Column(db.Text, nullable=True)
    symptom_duration = db.Column(db.String(100), nullable=True)
    symptom_severity = db.Column(db.String(50), nullable=True)
    associated_symptoms = db.Column(db.Text, nullable=True)
    
    # Medical History
    past_medical_conditions = db.Column(db.Text, nullable=True)
    previous_surgeries = db.Column(db.Text, nullable=True)
    hospitalizations = db.Column(db.Text, nullable=True)
    current_medications = db.Column(db.Text, nullable=True)
    allergies = db.Column(db.Text, nullable=True)
    
    # Lifestyle Factors
    diet_nutrition = db.Column(db.Text, nullable=True)
    physical_activity = db.Column(db.Text, nullable=True)
    sleep_patterns = db.Column(db.Text, nullable=True)
    stress_levels = db.Column(db.Text, nullable=True)
    substance_use = db.Column(db.Text, nullable=True)
    
    # Family Medical History
    family_medical_history = db.Column(db.Text, nullable=True)
    hereditary_conditions = db.Column(db.Text, nullable=True)
    
    # Medical Records Authorization
    medical_records_consent = db.Column(db.Boolean, default=False)
    authorized_providers = db.Column(db.Text, nullable=True)
    
    # System Information
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_consultation = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Patient {self.full_name}>'
    
    def to_dict(self):
        """Convert patient data to dictionary for easy JSON serialization."""
        return {
            'id': self.id,
            'full_name': self.full_name,
            'date_of_birth': self.date_of_birth,
            'address': self.address,
            'emergency_contact': self.emergency_contact,
            'temperature': self.temperature,
            'blood_pressure': self.blood_pressure,
            'heart_rate': self.heart_rate,
            'pain_level': self.pain_level,
            'chief_complaint': self.chief_complaint,
            'symptom_duration': self.symptom_duration,
            'symptom_severity': self.symptom_severity,
            'associated_symptoms': self.associated_symptoms,
            'past_medical_conditions': self.past_medical_conditions,
            'previous_surgeries': self.previous_surgeries,
            'hospitalizations': self.hospitalizations,
            'current_medications': self.current_medications,
            'allergies': self.allergies,
            'diet_nutrition': self.diet_nutrition,
            'physical_activity': self.physical_activity,
            'sleep_patterns': self.sleep_patterns,
            'stress_levels': self.stress_levels,
            'substance_use': self.substance_use,
            'family_medical_history': self.family_medical_history,
            'hereditary_conditions': self.hereditary_conditions,
            'medical_records_consent': self.medical_records_consent,
            'authorized_providers': self.authorized_providers,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'last_consultation': self.last_consultation.isoformat() if self.last_consultation else None
        }
    
    def get_summary(self):
        """Get a summary of patient information for AI context."""
        summary = f"Patient: {self.full_name}"
        if self.date_of_birth:
            summary += f", DOB: {self.date_of_birth}"
        if self.chief_complaint:
            summary += f", Chief Complaint: {self.chief_complaint}"
        if self.current_medications:
            summary += f", Current Medications: {self.current_medications}"
        if self.allergies:
            summary += f", Allergies: {self.allergies}"
        return summary


class ConsultationSession(db.Model):
    """Store individual consultation sessions and conversations."""
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    session_start = db.Column(db.DateTime, default=datetime.utcnow)
    session_end = db.Column(db.DateTime, nullable=True)
    conversation_history = db.Column(db.Text, nullable=True)  # JSON string of conversation
    report_generated = db.Column(db.Boolean, default=False)
    report_content = db.Column(db.Text, nullable=True)
    
    # Relationship
    patient = db.relationship('Patient', backref=db.backref('sessions', lazy=True))
    
    def __repr__(self):
        return f'<ConsultationSession {self.id} for Patient {self.patient_id}>'
    
    def get_conversation_history(self):
        """Get conversation history as a list of dictionaries."""
        if self.conversation_history:
            try:
                return json.loads(self.conversation_history)
            except json.JSONDecodeError:
                return []
        return []
    
    def set_conversation_history(self, history):
        """Set conversation history from a list of dictionaries."""
        self.conversation_history = json.dumps(history)
