
from flask import Flask, render_template, request, jsonify
import os
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


# Endpoint for advice (JSON)
@app.route('/get_advice', methods=['POST'])
def get_advice():
    data = request.json
    user_input = data.get('text', '')
    advice = get_medical_advice(user_input)
    return jsonify({'advice': advice})

# Endpoint for advice (plain text, for TTS)
@app.route('/speak_advice', methods=['POST'])
def speak_advice():
    data = request.json
    user_input = data.get('text', '')
    advice = get_medical_advice(user_input)
    return advice, 200, {'Content-Type': 'text/plain; charset=utf-8'}

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
