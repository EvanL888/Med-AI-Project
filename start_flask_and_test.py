#!/usr/bin/env python3
"""
Quick script to start Flask and test Sarah Thompson lookup
"""
import subprocess
import time
import requests
import threading
import os
import sys

def start_flask():
    """Start Flask app in background"""
    os.chdir("medAI")
    subprocess.run([sys.executable, "app.py"])

def test_sarah_lookup():
    """Test if Sarah Thompson can be found"""
    # Wait for Flask to start
    time.sleep(3)
    
    try:
        base_url = "http://localhost:5000"
        response = requests.post(f"{base_url}/lookup_patient",
                               json={"name": "Sarah Thompson"},
                               headers={'Content-Type': 'application/json'})
        
        if response.status_code == 200:
            result = response.json()
            if result.get('found'):
                print("✅ Sarah Thompson found in database!")
                patient = result.get('patient', {})
                print(f"   Name: {patient.get('full_name', 'N/A')}")
                print(f"   DOB: {patient.get('date_of_birth', 'N/A')}")
                print(f"   Address: {patient.get('address', 'N/A')}")
                return True
            else:
                print("❌ Sarah Thompson not found in database")
                return False
        else:
            print(f"❌ Error looking up patient: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error connecting to Flask app: {e}")
        return False

if __name__ == "__main__":
    print("🏥 Starting Flask app and testing Sarah Thompson lookup...")
    
    # Start Flask in background thread
    flask_thread = threading.Thread(target=start_flask, daemon=True)
    flask_thread.start()
    
    # Test lookup
    success = test_sarah_lookup()
    
    if not success:
        print("\n🔄 Sarah Thompson not found. You may need to run:")
        print("1. python add_test_data_api.py")
        print("2. python update_sarah_complete.py")
