#!/usr/bin/env python3
"""
Test the TTS voice functionality for the medical consultation.
"""

import requests
import json

def test_consultation_voice():
    """Test the voice functionality for consultation."""
    base_url = "http://localhost:5000"
    
    # Test different types of medical consultation messages
    test_messages = [
        "Welcome to your comprehensive medical consultation! I'm here to help you.",
        "What is your full name?",
        "Thank you. What is your date of birth?",
        "Can you describe your current symptoms?",
        "I understand. Let me ask about your medical history.",
        "Thank you for providing that information. Your consultation is now complete."
    ]
    
    print("🎤 Testing Medical Consultation Voice Messages")
    print("=" * 60)
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n{i}. Testing: '{message[:50]}{'...' if len(message) > 50 else ''}'")
        
        try:
            response = requests.post(f"{base_url}/text-to-speech", 
                                   json={"text": message},
                                   headers={'Content-Type': 'application/json'})
            
            if response.status_code == 200:
                result = response.json()
                audio_length = len(result.get('audio', ''))
                print(f"   ✅ Success! Audio generated: {audio_length} characters")
            else:
                print(f"   ❌ Error: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Exception: {e}")
    
    print("\n" + "=" * 60)
    print("✅ Voice testing complete!")
    print("\n🔊 Features implemented:")
    print("• Automatic TTS for robot's initial greeting")
    print("• All bot responses can be spoken automatically")
    print("• Click-to-speak icons on each bot message")
    print("• Toggle button to enable/disable auto-speech")
    print("• Azure OpenAI TTS with fallback to browser synthesis")
    
    print("\n🎯 To experience the voice consultation:")
    print("1. Go to http://localhost:5000/consultation")
    print("2. The robot will automatically speak its welcome message")
    print("3. All subsequent bot responses will be spoken")
    print("4. Use the 'Auto-Speech' toggle to control voice output")
    print("5. Click the 🔊 icon on any message to replay it")

if __name__ == "__main__":
    test_consultation_voice()
