
from flask import Flask, render_template, request, jsonify
import os
import sys
import openai
# Add the parent directory to the path to import secret_loader
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from secret_loader import load_secrets
# from azure.ai.textanalytics import TextAnalyticsClient  # Uncomment and configure if using Azure SDK
# from azure.core.credentials import AzureKeyCredential

app = Flask(__name__)

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
            azure_endpoint=secrets.AZURE_OPENAI_ENDPOINT,
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
    except Exception as e:
        return jsonify({'error': f'Error loading secrets: {str(e)}'}), 500
    
    try:
        print("Task started with Consultation Chat API")
        client = openai.AzureOpenAI(
            api_key=secrets.AZURE_OPENAI_API_KEY,
            api_version="2023-05-15",
            azure_endpoint=secrets.AZURE_OPENAI_ENDPOINT,
        )
        
        # Build conversation context
        messages = [
            {"role": "system", "content": """You are a medical assistant conducting a structured consultation. Your goal is to gather comprehensive information about the patient's health concerns and provide preliminary advice.

Follow this consultation structure:
1. First, ask about their main health concern or symptoms
2. Ask about symptom duration and severity (scale 1-10)
3. Ask about any related symptoms
4. Ask about their medical history and current medications
5. Ask about lifestyle factors (diet, exercise, sleep, stress)
6. Ask about allergies
7. Ask about family medical history if relevant
8. Provide a summary and preliminary recommendations

Ask ONE question at a time. Be empathetic and professional. After gathering sufficient information (usually 6-8 exchanges), offer to generate a consultation report."""}
        ]
        
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
        print("Task complete Consultation Chat API")
        return jsonify({"response": ai_message})
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
            azure_endpoint=secrets.AZURE_OPENAI_ENDPOINT,
        )
        
        # Create conversation summary for report generation
        conversation_text = "\n".join([f"{msg['role']}: {msg['content']}" for msg in conversation_history])
        
        messages = [
            {"role": "system", "content": """You are a medical assistant generating a consultation report. Based on the conversation provided, create a comprehensive medical consultation report with the following sections:

**MEDICAL CONSULTATION REPORT**

**Patient Information Summary:**
- Main complaints and symptoms
- Duration and severity of symptoms

**Medical History:**
- Current medications
- Previous medical conditions
- Allergies

**Lifestyle Factors:**
- Diet and nutrition
- Exercise habits
- Sleep patterns
- Stress levels

**Assessment:**
- Summary of key findings
- Potential concerns

**Recommendations:**
- Immediate actions
- Lifestyle modifications
- When to seek further medical attention

**Important Disclaimer:**
This is a preliminary assessment based on the information provided. Please consult with a qualified healthcare provider for proper diagnosis and treatment.

Format the report professionally and include all relevant information discussed during the consultation."""},
            {"role": "user", "content": f"Please generate a medical consultation report based on this conversation:\n\n{conversation_text}"}
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

