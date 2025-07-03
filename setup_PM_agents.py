#!/usr/bin/env python3
"""
Setup script for Property Manager agent only
"""

from dotenv import load_dotenv
load_dotenv()
import os

from vapi_agent import VapiAgent
from config import (
    PROPERTY_MANAGER_PHONE,
    PROPERTY_MANAGER_PROMPT,
    SERVER_URL
)

print("VAPI_PRIVATE_KEY:", os.environ.get("VAPI_PRIVATE_KEY"))

def setup_property_manager_agent():
    """Setup Property Manager agent only"""
    vapi = VapiAgent()
    try:
        print("🏗️ Setting up Property Manager agent...")
        # Create Property Manager assistant with webhook
        print("\n👔 Creating Property Manager agent...")
        property_manager = vapi.create_assistant(
            "Property Manager Agent",
            PROPERTY_MANAGER_PROMPT,
            server_url=SERVER_URL
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
        # Update Property Manager phone
        vapi.update_phone_number(
            property_manager_phone['id'],
            property_manager['id'],
            "Property Manager Phone"
        )
        print("\n✅ Setup completed successfully!")
        print(f"👔 Property Manager Agent ID: {property_manager['id']}")
        print(f"📞 Property Manager Phone ID: {property_manager_phone['id']}")
        setup_data = {
            'property_manager': {
                'assistant_id': property_manager['id'],
                'phone_id': property_manager_phone['id'],
                'phone_number': PROPERTY_MANAGER_PHONE
            }
        }
        print("\n📋 Setup data:", setup_data)
        return setup_data
    except Exception as e:
        print(f"❌ Setup failed: {e}")
        raise

def test_property_manager_call():
    """Test a call from Property Manager agent to the Indian number"""
    vapi = VapiAgent()
    try:
        print("📞 Testing Property Manager agent outbound call...")
        assistants = vapi.get_assistants()
        phone_numbers = vapi.get_phone_numbers()
        if not assistants or not phone_numbers:
            print("❌ No assistants or phone numbers found. Running setup first...")
            setup_property_manager_agent()
            return
        property_manager = None
        for assistant in assistants:
            if assistant['name'] == 'Property Manager Agent':
                property_manager = assistant
                break
        if not property_manager:
            print("❌ Property Manager agent not found. Running setup first...")
            setup_property_manager_agent()
            return
        property_manager_phone = None
        for phone in phone_numbers:
            if phone['number'] == PROPERTY_MANAGER_PHONE:
                property_manager_phone = phone
                break
        if not property_manager_phone:
            print("❌ Property Manager phone not found!")
            return
        DESTINATION_PHONE = "+918660186104"
        print(f"🚀 Initiating Property Manager → {DESTINATION_PHONE} call...")
        call = vapi.make_call(
            property_manager_phone['id'],
            DESTINATION_PHONE,
            property_manager['id']
        )
        print(f"✅ Call initiated: {call}")
    except Exception as e:
        print(f"❌ Call test failed: {e}")
        raise

if __name__ == "__main__":
    setup_property_manager_agent()
    test_property_manager_call() 