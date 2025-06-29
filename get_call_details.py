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
    # Use the call ID from our latest test
    call_id = "643f8296-c0e2-41c6-bbb2-08f64d9d8adf"
    get_call_details(call_id) 