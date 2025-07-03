from dotenv import load_dotenv
load_dotenv()

from flask import Flask, request, jsonify
from vapi_agent import VapiAgent
from config import (
    PROPERTY_MANAGER_PHONE, MAINTENANCE_PHONE,
    AZURE_OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT, AZURE_DEPLOYMENT_NAME,
    AZURE_OPENAI_GPT_API_KEY2, AZURE_OPENAI_GPT_ENDPOINT2, AZURE_GPT_DEPLOYMENT_NAME2
)
import json
from update_kb import add_conversation_to_kb
import chromadb
from azure_embedding import AzureOpenAIEmbeddingFunction
from openai import AzureOpenAI

# --- Validate Azure OpenAI config ---
if not AZURE_OPENAI_API_KEY or not AZURE_OPENAI_ENDPOINT or not AZURE_DEPLOYMENT_NAME:
    raise RuntimeError("Missing Azure OpenAI embedding credentials: check AZURE_OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT, AZURE_DEPLOYMENT_NAME in your .env file.")
if not AZURE_OPENAI_GPT_API_KEY2 or not AZURE_OPENAI_GPT_ENDPOINT2 or not AZURE_GPT_DEPLOYMENT_NAME2:
    raise RuntimeError("Missing Azure OpenAI GPT chat credentials: check AZURE_OPENAI_GPT_API_KEY2, AZURE_OPENAI_GPT_ENDPOINT2, AZURE_GPT_DEPLOYMENT_NAME2 in your .env file.")

app = Flask(__name__)
vapi = VapiAgent()

# Setup ChromaDB client and embedding function for RAG
chroma_client = chromadb.PersistentClient(path="./chroma_kb")
azure_ef = AzureOpenAIEmbeddingFunction(
    api_key=AZURE_OPENAI_API_KEY,
    endpoint=AZURE_OPENAI_ENDPOINT,
    deployment_name=AZURE_DEPLOYMENT_NAME
)
collection = chroma_client.get_collection("property_management_kb")

# Azure OpenAI client for LLM chat completions
chat_client = AzureOpenAI(
    api_key=AZURE_OPENAI_GPT_API_KEY2,
    api_version="2024-02-15-preview",
    azure_endpoint=AZURE_OPENAI_GPT_ENDPOINT2
)

def retrieve_similar(query, top_k=3):
    query_embedding = azure_ef([query])[0]
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "metadatas", "distances"]
    )
    docs = results["documents"][0] if results["documents"] else []
    return docs

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json or {}
    # Log the raw payload to a file for debugging
    with open('webhook_debug.log', 'a', encoding='utf-8') as f:
        import datetime
        f.write(f"\n--- {datetime.datetime.now().isoformat()} ---\n")
        f.write(json.dumps(data, indent=2, ensure_ascii=False))
        f.write("\n")
    print(f"[WEBHOOK] Received data: {json.dumps(data, indent=2)}")
    
    # Import real-time monitor
    try:
        from realtime_conversation import add_turn
    except ImportError:
        add_turn = None
    
    # Handle different VAPI webhook data structures
    user_message = None
    
    # Check for standard user message
    if 'user_message' in data:
        user_message = data['user_message']
        if add_turn:
            add_turn("User", user_message)
    elif 'text' in data:
        user_message = data['text']
        if add_turn:
            add_turn("User", user_message)
    elif 'data' in data and 'user_message' in data['data']:
        user_message = data['data']['user_message']
        if add_turn:
            add_turn("User", user_message)
    elif 'transcript' in data:
        # This is a transcript, store it in KB
        transcript = data['transcript']
        print(f"[WEBHOOK] Received transcript: {transcript}")
        
        # Parse transcript into conversation turns
        conversation_turns = []
        for line in transcript.split('\n'):
            if ': ' in line:
                role, message = line.split(': ', 1)
                conversation_turns.append({"role": role.strip(), "message": message.strip()})
                if add_turn:
                    add_turn(role.strip(), message.strip())
        
        if conversation_turns:
            add_conversation_to_kb(conversation_turns)
            print(f"[WEBHOOK] Added {len(conversation_turns)} turns to KB")
        
        return jsonify({"status": "transcript processed"})
    
    # Handle end-of-call-report with transcript
    elif data.get('event') == 'end-of-call-report' and 'transcript' in data:
        transcript = data['transcript']
        print(f"[WEBHOOK] Received end-of-call transcript: {transcript}")
        
        # Parse transcript into conversation turns
        conversation_turns = []
        for line in transcript.split('\n'):
            if ': ' in line:
                role, message = line.split(': ', 1)
                conversation_turns.append({"role": role.strip(), "message": message.strip()})
                if add_turn:
                    add_turn(role.strip(), message.strip())
        
        if conversation_turns:
            add_conversation_to_kb(conversation_turns)
            print(f"[WEBHOOK] Added {len(conversation_turns)} turns to KB")
        
        return jsonify({"status": "end-of-call transcript processed"})
    
    # Handle status-update with messages (new format)
    elif data.get('type') == 'status-update' and data.get('status') == 'ended':
        messages = data.get('artifact', {}).get('messages', [])
        print(f"[WEBHOOK] Received status-update with {len(messages)} messages")
        
        # Parse messages into conversation turns
        conversation_turns = []
        for msg in messages:
            if msg.get('role') in ['user', 'bot'] and msg.get('message'):
                role = "User" if msg['role'] == 'user' else "AI"
                conversation_turns.append({"role": role, "message": msg['message']})
                if add_turn:
                    add_turn(role, msg['message'])
        
        if conversation_turns:
            add_conversation_to_kb(conversation_turns)
            print(f"[WEBHOOK] Added {len(conversation_turns)} turns to KB from status-update")
        
        return jsonify({"status": "status-update processed"})
    
    # Handle nested message structure (alternative format)
    elif data.get('message', {}).get('type') == 'status-update' and data.get('message', {}).get('status') == 'ended':
        messages = data.get('message', {}).get('artifact', {}).get('messages', [])
        print(f"[WEBHOOK] Received nested status-update with {len(messages)} messages")
        
        # Parse messages into conversation turns
        conversation_turns = []
        for msg in messages:
            if msg.get('role') in ['user', 'bot'] and msg.get('message'):
                role = "User" if msg['role'] == 'user' else "AI"
                conversation_turns.append({"role": role, "message": msg['message']})
                if add_turn:
                    add_turn(role, msg['message'])
        
        if conversation_turns:
            add_conversation_to_kb(conversation_turns)
            print(f"[WEBHOOK] Added {len(conversation_turns)} turns to KB from nested status-update")
        
        return jsonify({"status": "nested status-update processed"})
    
    # Handle complete call data with messages in root structure
    elif 'messages' in data and isinstance(data['messages'], list):
        messages = data['messages']
        print(f"[WEBHOOK] Received complete call data with {len(messages)} messages")
        
        # Parse messages into conversation turns
        conversation_turns = []
        for msg in messages:
            if msg.get('role') in ['user', 'bot'] and msg.get('message'):
                role = "User" if msg['role'] == 'user' else "AI"
                conversation_turns.append({"role": role, "message": msg['message']})
                if add_turn:
                    add_turn(role, msg['message'])
        
        if conversation_turns:
            add_conversation_to_kb(conversation_turns)
            print(f"[WEBHOOK] Added {len(conversation_turns)} turns to KB from complete call data")
        
        return jsonify({"status": "complete call data processed"})
    
    if not user_message:
        print("[WEBHOOK] No user message found in data")
        return jsonify({"response": "I'm sorry, I didn't catch that. Could you please repeat?"})

    print(f"[WEBHOOK] Processing user message: {user_message}")
    
    # Use RAG to get relevant context
    context_docs = retrieve_similar(user_message, top_k=3)
    context = "\n".join(context_docs)

    prompt = (
        f"You are a helpful property manager. Use the following context to answer the user's question.\n"
        f"Context:\n{context}\n\n"
        f"User: {user_message}\n"
        f"Assistant:"
    )

    try:
        response = chat_client.chat.completions.create(
            model=AZURE_GPT_DEPLOYMENT_NAME2,
            messages=[{"role": "system", "content": prompt}],
            temperature=0.7,
            max_tokens=256
        )
        agent_reply = response.choices[0].message.content
        print(f"[WEBHOOK] Generated response: {agent_reply}")
        
        # Add AI response to real-time monitor
        if add_turn:
            add_turn("AI", agent_reply)
            
    except Exception as e:
        print(f"[ERROR] Azure OpenAI LLM call failed: {e}")
        return jsonify({"response": "Sorry, there was an error generating a response. Please try again later."})

    return jsonify({
        "response": agent_reply
    })

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
            MAINTENANCE_PHONE,
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

@app.route('/webhook/call_completed', methods=['POST'])
def call_completed_webhook():
    data = request.json or {}
    transcript = data.get('transcript', '')
    if not transcript:
        return jsonify({"status": "no transcript"}), 400

    # Parse transcript into conversation turns
    conversation_turns = []
    for line in transcript.split('\n'):
        if ': ' in line:
            role, message = line.split(': ', 1)
            conversation_turns.append({"role": role.strip(), "message": message.strip()})

    if conversation_turns:
        add_conversation_to_kb(conversation_turns)
        return jsonify({"status": "added to KB"}), 200
    else:
        return jsonify({"status": "no valid turns"}), 400

if __name__ == '__main__':
    print("Vapi voice agent server starting...")
    print("Webhook URL: http://localhost:5000/webhook")
    print("Trigger call: POST http://localhost:5000/trigger-call")
    print("Setup: POST http://localhost:5000/setup")
    print("Health check: GET http://localhost:5000/health")
    
    app.run(debug=True, host='0.0.0.0', port=5000) 