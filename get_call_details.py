#!/usr/bin/env python3
"""
Get detailed information about a specific call
"""

from vapi_agent import VapiAgent
import json
import requests

def get_call_details(call_id):
    """Get detailed information about a specific call"""
    vapi = VapiAgent()
    
    try:
        print(f"📞 Getting details for call: {call_id}")
        url = f"{vapi.base_url}/call/{call_id}"
        response = requests.get(url, headers=vapi.headers)
        response.raise_for_status()
        
        call_details = response.json()
        print("\n📋 Call Details:")
        print(json.dumps(call_details, indent=2))
        
        return call_details
        
    except Exception as e:
        print(f"Error getting call details: {e}")
        return None

if __name__ == "__main__":
    # Use the call ID from our previous test
    call_id = "baa254da-e42f-47ca-8670-4c3e12a49259"
    get_call_details(call_id) 