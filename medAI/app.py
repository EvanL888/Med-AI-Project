
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

# Endpoint for advice (plain text, for TTS)
@app.route('/speak_advice', methods=['POST'])
def speak_advice():
    data = request.json
    user_input = data.get('text', '')
    advice = get_medical_advice(user_input)
    return advice, 200, {'Content-Type': 'text/plain; charset=utf-8'}



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

