from vapi_agent import VapiAgent
from config import SOURCE_PHONE_NUMBER, DESTINATION_PHONE_NUMBER

def setup_vapi_agent():
    """Setup a single Vapi agent and use existing phone numbers"""
    vapi = VapiAgent()
    
    try:
        print("Setting up Vapi voice agent...")
        
        # Create single voice assistant
        print("Creating voice assistant...")
        assistant = vapi.create_assistant(
            "Voice Agent",
            "You are a helpful voice assistant. When you make a call, greet the person warmly and ask how you can help them. Keep responses brief and natural. After a brief conversation, politely end the call."
        )
        
        # Get existing phone numbers
        print("Getting existing phone numbers...")
        phone_numbers = vapi.get_phone_numbers()
        
        # Find source phone number
        source_phone = None
        for phone in phone_numbers:
            if phone['number'] == SOURCE_PHONE_NUMBER:
                source_phone = phone
                break
        
        if not source_phone:
            print(f"Source phone number {SOURCE_PHONE_NUMBER} not found!")
            return None
        
        print("Setup completed successfully!")
        print(f"Assistant ID: {assistant['id']}")
        print(f"Source Phone ID: {source_phone['id']}")
        print(f"Destination Phone: {DESTINATION_PHONE_NUMBER}")
        
        # Save the IDs for later use
        setup_data = {
            'assistant_id': assistant['id'],
            'source_phone_id': source_phone['id'],
            'destination_phone': DESTINATION_PHONE_NUMBER
        }
        
        print("Setup data:", setup_data)
        return setup_data
        
    except Exception as e:
        print(f"Setup failed: {e}")
        raise

def test_call():
    """Test a call from source to destination"""
    vapi = VapiAgent()
    
    try:
        print("Testing call from source to destination...")
        
        # Get existing assistants and phone numbers
        assistants = vapi.get_assistants()
        phone_numbers = vapi.get_phone_numbers()
        
        if not assistants or not phone_numbers:
            print("No assistants or phone numbers found. Running setup first...")
            setup_vapi_agent()
            return
        
        # Find the voice assistant and source phone number
        voice_assistant = None
        for assistant in assistants:
            if assistant['name'] == 'Voice Agent':
                voice_assistant = assistant
                break
        
        if not voice_assistant:
            voice_assistant = assistants[0]  # Use first assistant if Voice Agent not found
        
        source_phone = None
        for phone in phone_numbers:
            if phone['number'] == SOURCE_PHONE_NUMBER:
                source_phone = phone
                break
        
        if not source_phone:
            print(f"Source phone number {SOURCE_PHONE_NUMBER} not found!")
            return
        
        print("Initiating call...")
        call = vapi.make_call(
            source_phone['id'],
            DESTINATION_PHONE_NUMBER,
            voice_assistant['id']
        )
        
        print(f"Call initiated: {call}")
        
    except Exception as e:
        print(f"Test call failed: {e}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "setup":
            setup_vapi_agent()
        elif command == "test":
            test_call()
        else:
            print("Usage:")
            print("  python setup.py setup  - Setup voice agent and use existing phone numbers")
            print("  python setup.py test   - Test a call from source to destination")
    else:
        print("Usage:")
        print("  python setup.py setup  - Setup voice agent and use existing phone numbers")
        print("  python setup.py test   - Test a call from source to destination") 