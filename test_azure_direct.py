#!/usr/bin/env python3
"""
Simple test to check the speech-to-text endpoint directly
"""

import sys
import os
sys.path.append('.')

from secret_loader import load_secrets
import httpx

def test_azure_stt_endpoint():
    """Test the Azure STT endpoint directly"""
    
    print("=== DIRECT AZURE STT ENDPOINT TEST ===")
    
    try:
        secrets = load_secrets()
        
        print(f"STT Endpoint: {secrets.AZURE_SPEECH_STT_ENDPOINT}")
        print(f"STT Key present: {'Yes' if secrets.AZURE_SPEECH_STT_KEY else 'No'}")
        print(f"STT Key length: {len(secrets.AZURE_SPEECH_STT_KEY) if secrets.AZURE_SPEECH_STT_KEY else 0}")
        print(f"STT Region: {secrets.AZURE_SPEECH_STT_REGION}")
        
        # Test with a small audio file
        wav_file_path = "wikipediaOcelot.wav"
        
        if not os.path.exists(wav_file_path):
            print(f"ERROR: WAV file not found at {wav_file_path}")
            return False
        
        # Read the audio file
        with open(wav_file_path, 'rb') as audio_file:
            audio_content = audio_file.read()
        
        print(f"Audio file size: {len(audio_content)} bytes")
        
        # Try the OpenAI Whisper format (based on the endpoint URL)
        print("Testing with OpenAI Whisper format...")
        
        files = {
            'file': ('wikipediaOcelot.wav', audio_content, 'audio/wav')
        }
        headers = {
            'api-key': secrets.AZURE_SPEECH_STT_KEY
        }
        
        stt_url = secrets.AZURE_SPEECH_STT_ENDPOINT
        
        print(f"Making request to: {stt_url}")
        
        with httpx.Client(timeout=60.0) as client:
            resp = client.post(stt_url, files=files, headers=headers)
        
        print(f"Response status: {resp.status_code}")
        print(f"Response headers: {dict(resp.headers)}")
        
        if resp.status_code == 200:
            result = resp.json()
            print(f"SUCCESS! Response: {result}")
            transcribed_text = result.get('text', '')
            print(f"Transcribed text: '{transcribed_text}'")
            return True
        else:
            print(f"ERROR: {resp.status_code}")
            print(f"Response content: {resp.text}")
            return False
            
    except Exception as e:
        print(f"Exception: {e}")
        return False

if __name__ == "__main__":
    success = test_azure_stt_endpoint()
    if success:
        print("\n🎉 Direct Azure test successful!")
    else:
        print("\n❌ Direct Azure test failed.")
