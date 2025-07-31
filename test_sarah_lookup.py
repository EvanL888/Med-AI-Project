#!/usr/bin/env python3
"""
Quick test to verify Sarah Thompson is in database and can generate reports
"""
import requests
import json

def test_sarah_thompson():
    """Test Sarah Thompson lookup and basic report generation"""
    base_url = "http://localhost:5000"
    
    print("🔍 Testing Sarah Thompson lookup...")
    
    # Test patient lookup
    lookup_response = requests.post(f"{base_url}/lookup_patient",
                                  json={"name": "Sarah Thompson"},
                                  headers={'Content-Type': 'application/json'})
    
    if lookup_response.status_code == 200:
        result = lookup_response.json()
        if result.get('found'):
            print("✅ Sarah Thompson found in database!")
            patient = result.get('patient', {})
            print(f"   Name: {patient.get('full_name', 'N/A')}")
            print(f"   DOB: {patient.get('date_of_birth', 'N/A')}")
            print(f"   Chief Complaint: {patient.get('chief_complaint', 'N/A')}")
            print(f"   Medications: {patient.get('current_medications', 'N/A')}")
            
            # Test basic report generation with simple conversation
            print("\n📋 Testing report generation...")
            test_conversation = [
                {"role": "assistant", "content": "Hello! What's your name?"},
                {"role": "user", "content": "Sarah Thompson"},
                {"role": "assistant", "content": "How are you feeling today?"},
                {"role": "user", "content": "I'm having some stomach pain."}
            ]
            
            report_response = requests.post(f"{base_url}/generate_report",
                                          json={"history": test_conversation},
                                          headers={'Content-Type': 'application/json'})
            
            if report_response.status_code == 200:
                print("✅ Report generation working!")
                report_data = report_response.json()
                report = report_data.get('report', '')
                print("📄 Sample report preview:")
                print(report[:300] + "..." if len(report) > 300 else report)
                return True
            else:
                print(f"❌ Report generation failed: {report_response.status_code}")
                print(f"   Error: {report_response.text}")
                return False
        else:
            print("❌ Sarah Thompson not found")
            return False
    else:
        print(f"❌ Lookup failed: {lookup_response.status_code}")
        return False

if __name__ == "__main__":
    test_sarah_thompson()
