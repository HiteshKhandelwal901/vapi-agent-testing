#!/usr/bin/env python3
"""
Check call status and logs from Vapi
"""

from vapi_agent import VapiAgent
import json

def check_calls():
    """Check recent calls and their status"""
    vapi = VapiAgent()
    
    try:
        print("📊 Checking recent calls...")
        calls = vapi.get_calls()
        
        if calls:
            print(f"Found {len(calls)} recent calls:")
            for call in calls:
                print(f"\nCall ID: {call.get('id')}")
                print(f"Status: {call.get('status')}")
                print(f"From: {call.get('from')}")
                print(f"To: {call.get('to')}")
                print(f"Created: {call.get('createdAt')}")
                print(f"Duration: {call.get('duration')} seconds")
                print("-" * 40)
        else:
            print("No recent calls found.")
            
    except Exception as e:
        print(f"Error checking calls: {e}")

if __name__ == "__main__":
    check_calls() 