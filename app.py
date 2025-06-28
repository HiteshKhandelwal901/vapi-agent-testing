from flask import Flask, request, jsonify
from vapi_agent import VapiAgent
from config import SOURCE_PHONE_NUMBER, DESTINATION_PHONE_NUMBER
import json

app = Flask(__name__)
vapi = VapiAgent()

# Basic conversation state to track message exchanges
conversation_count = 0
MAX_EXCHANGES = 3  # Exit after 3 exchanges

def get_llm_response(user_message):
    """Simple LLM response function for the voice agent"""
    responses = [
        "Hello! This is your voice assistant. How can I help you today?",
        "I understand your request. Let me assist you with that.",
        "Thank you for the conversation. Have a great day!"
    ]
    
    current_index = min(conversation_count, len(responses) - 1)
    return responses[current_index]

@app.route('/webhook', methods=['POST'])
def webhook():
    """Handle Vapi webhooks"""
    global conversation_count
    
    print(f"Received webhook: {json.dumps(request.json, indent=2)}")
    
    data = request.json
    event_type = data.get('type')
    
    if event_type == 'call-start':
        conversation_count = 0
        call_data = data.get('call', {})
        from_number = call_data.get('from')
        to_number = call_data.get('to')
        
        print(f"Call started from {from_number} to {to_number}")
        
        response = get_llm_response('')
        
        return jsonify({
            'assistant': {
                'name': 'Voice Agent',
                'model': {
                    'provider': 'openai',
                    'model': 'gpt-3.5-turbo',
                    'systemPrompt': 'You are a helpful voice assistant. When you make a call, greet the person warmly and ask how you can help them. Keep responses brief and natural. After a brief conversation, politely end the call.'
                },
                'voice': {
                    'provider': '11labs',
                    'voiceId': 'pNInz6obpgDQGcFmaJgB'
                },
                'firstMessage': response
            }
        })
    
    elif event_type == 'call-end':
        print("Call ended")
        return jsonify({})
    
    elif event_type == 'function-call':
        # Handle function calls if needed
        return jsonify({})
    
    else:
        return jsonify({})

@app.route('/trigger-call', methods=['POST'])
def trigger_call():
    """Trigger a call from source to destination"""
    try:
        # Get existing assistants and phone numbers
        assistants = vapi.get_assistants()
        phone_numbers = vapi.get_phone_numbers()
        
        if not assistants or not phone_numbers:
            return jsonify({'error': 'No assistants or phone numbers found. Run setup first.'}), 400
        
        # Use the first assistant and source phone number
        assistant = assistants[0]
        source_phone = phone_numbers[0]  # Assuming first phone number is source
        
        print("Initiating call from source to destination...")
        call = vapi.make_call(
            source_phone['id'],
            DESTINATION_PHONE_NUMBER,
            assistant['id']
        )
        
        return jsonify({
            'message': 'Call initiated successfully from source to destination',
            'call': call
        })
        
    except Exception as e:
        print(f"Error triggering call: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'message': 'Vapi voice agent is running'
    })

@app.route('/setup', methods=['POST'])
def setup_endpoint():
    """Setup endpoint to create agent and phone number"""
    try:
        from setup import setup_vapi_agent
        setup_data = setup_vapi_agent()
        return jsonify({
            'message': 'Setup completed successfully',
            'data': setup_data
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("Vapi voice agent server starting...")
    print("Webhook URL: http://localhost:5000/webhook")
    print("Trigger call: POST http://localhost:5000/trigger-call")
    print("Setup: POST http://localhost:5000/setup")
    print("Health check: GET http://localhost:5000/health")
    
    app.run(debug=True, host='0.0.0.0', port=5000) 