from flask import Flask, request, jsonify
from vapi_agent import VapiAgent
from config import PROPERTY_MANAGER_PHONE, MAINTENANCE_PHONE, AZURE_OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT, AZURE_DEPLOYMENT_NAME
import json
from update_kb import add_conversation_to_kb
from openai import OpenAI
import chromadb
from azure_embedding import AzureOpenAIEmbeddingFunction

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

# OpenAI client for LLM calls
client = OpenAI(api_key=AZURE_OPENAI_API_KEY)

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
    data = request.json
    # Extract the user message (adjust key as per Vapi's payload)
    user_message = data.get('user_message', '')
    if not user_message:
        # Fallback: try to extract from other fields or return default
        user_message = data.get('text', '')
    if not user_message:
        return jsonify({"response": "I'm sorry, I didn't catch that. Could you please repeat?"})

    # 1. Retrieve relevant context from ChromaDB
    context_docs = retrieve_similar(user_message, top_k=3)
    context = "\n".join(context_docs)

    # 2. Compose the prompt for the LLM
    prompt = (
        f"You are a helpful property manager. Use the following context to answer the user's question.\n"
        f"Context:\n{context}\n\n"
        f"User: {user_message}\n"
        f"Assistant:"
    )

    # 3. Call the LLM (OpenAI v1.x syntax)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": prompt}]
    )
    agent_reply = response.choices[0].message.content

    # 4. Return the reply to Vapi
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
    data = request.json
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