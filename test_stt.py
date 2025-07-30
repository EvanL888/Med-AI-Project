#!/usr/bin/env python3
"""
Test script for speech-to-text functionality using the existing WAV file.
This will help diagnose issues with the STT endpoint.
"""

import requests
import os
import sys

def test_speech_to_text():
    """Test the speech-to-text endpoint with the existing WAV file."""
    
    # File paths
    wav_file_path = "wikipediaOcelot.wav"
    flask_url = "http://localhost:5000/speech-to-text"
    
    print("=== SPEECH-TO-TEXT TEST STARTED ===")
    print(f"Testing with file: {wav_file_path}")
    
    # Check if file exists
    if not os.path.exists(wav_file_path):
        print(f"ERROR: WAV file not found at {wav_file_path}")
        return False
    
    # Get file info
    file_size = os.path.getsize(wav_file_path)
    print(f"File size: {file_size} bytes")
    
    try:
        # Prepare the file for upload
        with open(wav_file_path, 'rb') as audio_file:
            files = {
                'file': ('wikipediaOcelot.wav', audio_file, 'audio/wav')
            }
            
            print(f"Making POST request to: {flask_url}")
            print("Uploading audio file...")
            
            # Make the request
            response = requests.post(flask_url, files=files, timeout=60)
            
            print(f"Response status code: {response.status_code}")
            print(f"Response headers: {dict(response.headers)}")
            
            if response.status_code == 200:
                result = response.json()
                print("SUCCESS! Response received:")
                print(f"Transcription: '{result.get('transcription', 'No transcription found')}'")
                print("=== SPEECH-TO-TEXT TEST COMPLETED SUCCESSFULLY ===")
                return True
            else:
                print(f"ERROR: HTTP {response.status_code}")
                print(f"Response content: {response.text}")
                print("=== SPEECH-TO-TEXT TEST FAILED ===")
                return False
                
    except requests.exceptions.ConnectionError:
        print("ERROR: Could not connect to Flask server.")
        print("Make sure the Flask app is running on http://localhost:5000")
        print("Run: python medAI/app.py")
        return False
    except requests.exceptions.Timeout:
        print("ERROR: Request timed out (60 seconds)")
        return False
    except Exception as e:
        print(f"ERROR: Unexpected exception: {e}")
        return False

def check_flask_server():
    """Check if Flask server is running."""
    try:
        response = requests.get("http://localhost:5000/", timeout=5)
        if response.status_code == 200:
            print("✓ Flask server is running")
            return True
        else:
            print(f"✗ Flask server responded with status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("✗ Flask server is not running")
        return False
    except Exception as e:
        print(f"✗ Error checking Flask server: {e}")
        return False

if __name__ == "__main__":
    print("Starting Speech-to-Text Test")
    print("=" * 50)
    
    # Check if Flask server is running
    if not check_flask_server():
        print("\nPlease start the Flask server first:")
        print("cd medAI")
        print("python app.py")
        sys.exit(1)
    
    # Run the test
    success = test_speech_to_text()
    
    if success:
        print("\n🎉 Test completed successfully!")
    else:
        print("\n❌ Test failed. Check the error messages above.")
        sys.exit(1)
