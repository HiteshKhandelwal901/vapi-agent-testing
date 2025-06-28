#!/usr/bin/env python3
"""
Check what's configured for the destination phone number
"""

from vapi_agent import VapiAgent
from config import DESTINATION_PHONE_NUMBER
import json

def check_destination_config():
    """Check what's configured for the destination phone number"""
    vapi = VapiAgent()
    
    try:
        print(f"🔍 Checking configuration for destination: {DESTINATION_PHONE_NUMBER}")
        
        # Get all phone numbers
        phone_numbers = vapi.get_phone_numbers()
        
        if phone_numbers:
            print(f"\n📱 Found {len(phone_numbers)} phone numbers:")
            for phone in phone_numbers:
                print(f"\nPhone: {phone.get('number')}")
                print(f"ID: {phone.get('id')}")
                print(f"Name: {phone.get('name')}")
                print(f"Assistant ID: {phone.get('assistantId')}")
                print(f"Status: {phone.get('status')}")
                
                # Check if this is our destination
                if phone.get('number') == DESTINATION_PHONE_NUMBER:
                    print("🎯 This is our destination number!")
                    if phone.get('assistantId'):
                        print("🤖 This number has an assistant configured!")
                    else:
                        print("📞 This number has no assistant configured")
                print("-" * 40)
        else:
            print("No phone numbers found.")
            
    except Exception as e:
        print(f"Error checking destination: {e}")

if __name__ == "__main__":
    check_destination_config() 