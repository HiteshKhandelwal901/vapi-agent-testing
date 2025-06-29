#!/usr/bin/env python3
"""
Setup script for Property Manager and Maintenance agents
"""

from vapi_agent import VapiAgent
from config import (
    PROPERTY_MANAGER_PHONE, 
    MAINTENANCE_PHONE,
    PROPERTY_MANAGER_PROMPT,
    MAINTENANCE_AGENT_PROMPT
)

def setup_two_agents():
    """Setup Property Manager and Maintenance agents"""
    vapi = VapiAgent()
    
    try:
        print("🏗️ Setting up Property Manager and Maintenance agents...")
        
        # Create Property Manager assistant
        print("\n👔 Creating Property Manager agent...")
        property_manager = vapi.create_assistant(
            "Property Manager Agent",
            PROPERTY_MANAGER_PROMPT
        )
        
        # Create Maintenance assistant
        print("\n🔧 Creating Maintenance agent...")
        maintenance_agent = vapi.create_assistant(
            "Maintenance Agent",
            MAINTENANCE_AGENT_PROMPT
        )
        
        # Get existing phone numbers
        print("\n📱 Getting existing phone numbers...")
        phone_numbers = vapi.get_phone_numbers()
        
        if not phone_numbers:
            print("❌ No phone numbers found!")
            return None
        
        # Find and configure Property Manager phone
        property_manager_phone = None
        for phone in phone_numbers:
            if phone['number'] == PROPERTY_MANAGER_PHONE:
                property_manager_phone = phone
                break
        
        if not property_manager_phone:
            print(f"❌ Property Manager phone {PROPERTY_MANAGER_PHONE} not found!")
            return None
        
        # Find and configure Maintenance phone
        maintenance_phone = None
        for phone in phone_numbers:
            if phone['number'] == MAINTENANCE_PHONE:
                maintenance_phone = phone
                break
        
        if not maintenance_phone:
            print(f"❌ Maintenance phone {MAINTENANCE_PHONE} not found!")
            return None
        
        # Update phone numbers to associate with their respective assistants
        print("\n🔗 Associating phone numbers with agents...")
        
        # Update Property Manager phone
        vapi.update_phone_number(
            property_manager_phone['id'],
            property_manager['id'],
            "Property Manager Phone"
        )
        
        # Update Maintenance phone
        vapi.update_phone_number(
            maintenance_phone['id'],
            maintenance_agent['id'],
            "Maintenance Phone"
        )
        
        print("\n✅ Setup completed successfully!")
        print(f"👔 Property Manager Agent ID: {property_manager['id']}")
        print(f"📞 Property Manager Phone ID: {property_manager_phone['id']}")
        print(f"🔧 Maintenance Agent ID: {maintenance_agent['id']}")
        print(f"📞 Maintenance Phone ID: {maintenance_phone['id']}")
        
        # Save the setup data
        setup_data = {
            'property_manager': {
                'assistant_id': property_manager['id'],
                'phone_id': property_manager_phone['id'],
                'phone_number': PROPERTY_MANAGER_PHONE
            },
            'maintenance': {
                'assistant_id': maintenance_agent['id'],
                'phone_id': maintenance_phone['id'],
                'phone_number': MAINTENANCE_PHONE
            }
        }
        
        print("\n📋 Setup data:", setup_data)
        return setup_data
        
    except Exception as e:
        print(f"❌ Setup failed: {e}")
        raise

def test_agent_call():
    """Test a call from Property Manager to Maintenance agent"""
    vapi = VapiAgent()
    
    try:
        print("📞 Testing Property Manager → Maintenance agent call...")
        
        # Get existing assistants and phone numbers
        assistants = vapi.get_assistants()
        phone_numbers = vapi.get_phone_numbers()
        
        if not assistants or not phone_numbers:
            print("❌ No assistants or phone numbers found. Running setup first...")
            setup_two_agents()
            return
        
        # Find the agents
        property_manager = None
        maintenance_agent = None
        
        for assistant in assistants:
            if assistant['name'] == 'Property Manager Agent':
                property_manager = assistant
            elif assistant['name'] == 'Maintenance Agent':
                maintenance_agent = assistant
        
        if not property_manager or not maintenance_agent:
            print("❌ Agents not found. Running setup first...")
            setup_two_agents()
            return
        
        # Find the phone numbers
        property_manager_phone = None
        maintenance_phone = None
        
        for phone in phone_numbers:
            if phone['number'] == PROPERTY_MANAGER_PHONE:
                property_manager_phone = phone
            elif phone['number'] == MAINTENANCE_PHONE:
                maintenance_phone = phone
        
        if not property_manager_phone or not maintenance_phone:
            print("❌ Phone numbers not found!")
            return
        
        print("🚀 Initiating Property Manager → Maintenance call...")
        call = vapi.make_call(
            property_manager_phone['id'],
            MAINTENANCE_PHONE,
            property_manager['id']
        )
        
        print(f"✅ Call initiated: {call}")
        print("⏱️ Call will last approximately 30 seconds...")
        
    except Exception as e:
        print(f"❌ Test call failed: {e}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "setup":
            setup_two_agents()
        elif command == "test":
            test_agent_call()
        else:
            print("Usage:")
            print("  python setup_two_agents.py setup  - Setup both agents")
            print("  python setup_two_agents.py test   - Test Property Manager → Maintenance call")
    else:
        print("Usage:")
        print("  python setup_two_agents.py setup  - Setup both agents")
        print("  python setup_two_agents.py test   - Test Property Manager → Maintenance call") 