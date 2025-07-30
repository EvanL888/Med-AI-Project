#!/usr/bin/env python3
"""
Script to add test patient data via HTTP requests to the running Flask app.
This approach avoids database context issues.
"""

import requests
import json
from datetime import datetime

def add_sarah_thompson_via_api():
    """Add Sarah Thompson's data via the Flask API endpoints."""
    
    base_url = "http://localhost:5000"
    
    # First, create the consultation conversation history
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
        {"role": "user", "content": "128 over 82 mmHg"},
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
    
    # Save the patient data
    save_data = {
        "name": "Sarah Thompson",
        "history": conversation_history
    }
    
    try:
        print("🏥 Adding Sarah Thompson's test data via API...")
        print("=" * 60)
        
        # Make the API call to save patient
        response = requests.post(f"{base_url}/save_patient", 
                               json=save_data,
                               headers={'Content-Type': 'application/json'})
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Successfully added Sarah Thompson's medical data!")
            print(f"   Patient ID: {result.get('patient_id')}")
            print(f"   Session ID: {result.get('session_id')}")
            print(f"   Total conversation exchanges: {len(conversation_history)}")
            
            # Test patient lookup
            print("\n🔍 Testing patient lookup...")
            lookup_response = requests.post(f"{base_url}/lookup_patient",
                                          json={"name": "Sarah Thompson"},
                                          headers={'Content-Type': 'application/json'})
            
            if lookup_response.status_code == 200:
                lookup_result = lookup_response.json()
                if lookup_result.get('found'):
                    print("✅ Patient lookup successful!")
                    print(f"   Patient found: {lookup_result.get('patient', {}).get('full_name')}")
                    print(f"   Last consultation: {lookup_result.get('last_consultation')}")
                    print(f"   Summary: {lookup_result.get('summary', 'No summary available')}")
                else:
                    print("❌ Patient not found in lookup test")
            
            return True
            
        else:
            print(f"❌ Error saving patient: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to Flask app. Make sure it's running on http://localhost:5000")
        print("\nTo start the Flask app:")
        print("1. Open a new terminal")
        print("2. Navigate to the medAI directory")
        print("3. Run: python app.py")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Main function to add test data."""
    print("🔬 Medical AI Test Data Insertion")
    print("This script will add Sarah Thompson's comprehensive medical data")
    print("to your Medical AI database via API calls.\n")
    
    success = add_sarah_thompson_via_api()
    
    if success:
        print("\n" + "=" * 60)
        print("✅ Test data addition completed successfully!")
        print("\nYou can now test the patient recognition by:")
        print("1. Going to http://localhost:5000/consultation")
        print("2. Starting a new consultation")
        print("3. When asked for your name, enter 'Sarah Thompson'")
        print("4. The system should recognize her and load existing data")
        print("5. You can continue the consultation or generate a report")
    else:
        print("\n❌ Test data addition failed.")
        print("Please ensure the Flask app is running and try again.")

if __name__ == "__main__":
    main()
