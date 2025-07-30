#!/usr/bin/env python3
"""
Script to manually update Sarah Thompson's complete medical data.
This will ensure all her comprehensive information is properly stored.
"""

import requests
import json

def update_sarah_thompson_complete_data():
    """Update Sarah Thompson with all missing data via direct API call."""
    
    # First, get her current data
    base_url = "http://localhost:5000"
    
    # Get current patient data
    lookup_response = requests.post(f"{base_url}/lookup_patient",
                                  json={"name": "Sarah Thompson"},
                                  headers={'Content-Type': 'application/json'})
    
    if lookup_response.status_code != 200 or not lookup_response.json().get('found'):
        print("❌ Sarah Thompson not found in database. Please run add_test_data_api.py first.")
        return False
    
    current_data = lookup_response.json()['patient']
    print(f"📋 Current data for Sarah Thompson (ID: {current_data['id']}):")
    
    # Create comprehensive conversation history that includes ALL the missing data
    comprehensive_conversation = [
        {"role": "assistant", "content": "Hello! I'm your medical assistant. Could you please tell me your full name?"},
        {"role": "user", "content": "My name is Sarah Thompson"},
        {"role": "assistant", "content": "Thank you, Sarah. What is your date of birth?"},
        {"role": "user", "content": "My date of birth is April 15th, 1985, which is 04/15/1985"},
        {"role": "assistant", "content": "What is your current address?"},
        {"role": "user", "content": "My current address is 127 Maplewood Lane, Edison, NJ 08820"},
        {"role": "assistant", "content": "Could you provide emergency contact information?"},
        {"role": "user", "content": "John Thompson, my spouse, at (732) 555-9123"},
        {"role": "assistant", "content": "What is your current temperature if you've taken it?"},
        {"role": "user", "content": "My current temperature is 98.6 degrees Fahrenheit"},
        {"role": "assistant", "content": "Do you have a recent blood pressure reading?"},
        {"role": "user", "content": "My blood pressure reading is 128 over 82 mmHg"},
        {"role": "assistant", "content": "What about your heart rate or pulse?"},
        {"role": "user", "content": "My heart rate is 78 beats per minute"},
        {"role": "assistant", "content": "On a scale of 1-10, what is your current pain level?"},
        {"role": "user", "content": "About a 4 out of 10, I have mild abdominal discomfort"},
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
    
    # Save the updated conversation to trigger better extraction
    save_data = {
        "name": "Sarah Thompson",
        "history": comprehensive_conversation
    }
    
    print("🔄 Updating Sarah Thompson's data with comprehensive information...")
    response = requests.post(f"{base_url}/save_patient", 
                           json=save_data,
                           headers={'Content-Type': 'application/json'})
    
    if response.status_code == 200:
        result = response.json()
        print("✅ Successfully updated Sarah Thompson's comprehensive data!")
        
        # Verify the update
        updated_lookup = requests.post(f"{base_url}/lookup_patient",
                                     json={"name": "Sarah Thompson"},
                                     headers={'Content-Type': 'application/json'})
        
        if updated_lookup.status_code == 200:
            updated_data = updated_lookup.json()['patient']
            print("\n📊 Updated patient data:")
            print(f"   Name: {updated_data['full_name']}")
            print(f"   DOB: {updated_data['date_of_birth']}")
            print(f"   Address: {updated_data['address']}")
            print(f"   Emergency Contact: {updated_data['emergency_contact']}")
            print(f"   Temperature: {updated_data['temperature']}")
            print(f"   Blood Pressure: {updated_data['blood_pressure']}")
            print(f"   Heart Rate: {updated_data['heart_rate']}")
            print(f"   Pain Level: {updated_data['pain_level']}")
            print(f"   Chief Complaint: {updated_data['chief_complaint']}")
            print(f"   Past Conditions: {updated_data['past_medical_conditions']}")
            print(f"   Current Medications: {updated_data['current_medications']}")
            print(f"   Allergies: {updated_data['allergies']}")
            return True
        
    else:
        print(f"❌ Error updating patient: {response.status_code}")
        print(f"   Response: {response.text}")
        return False

def main():
    """Main function to update comprehensive data."""
    print("🏥 Updating Sarah Thompson's Comprehensive Medical Data")
    print("=" * 60)
    
    try:
        success = update_sarah_thompson_complete_data()
        if success:
            print("\n" + "=" * 60)
            print("✅ Comprehensive data update completed successfully!")
            print("\nSarah Thompson now has complete medical information including:")
            print("• Patient identification (name, DOB, address, emergency contact)")
            print("• Vital signs (temperature, blood pressure, heart rate, pain level)")
            print("• Chief complaint and symptoms")
            print("• Medical history (conditions, surgeries, hospitalizations)")
            print("• Current medications and allergies")
            print("• Lifestyle factors")
            print("• Family medical history")
            print("• Medical records authorization")
            
            print(f"\n🎯 Test the system by:")
            print(f"1. Going to http://localhost:5000/consultation")
            print(f"2. Enter 'Sarah Thompson' when asked for your name")
            print(f"3. The system will recognize her with all comprehensive data")
        else:
            print("\n❌ Failed to update comprehensive data")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
