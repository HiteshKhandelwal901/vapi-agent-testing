import requests
import json
from config import VAPI_PRIVATE_KEY, VAPI_BASE_URL

class VapiAgent:
    def __init__(self):
        self.base_url = VAPI_BASE_URL
        self.private_key = VAPI_PRIVATE_KEY
        self.headers = {
            'Authorization': f'Bearer {self.private_key}',
            'Content-Type': 'application/json'
        }
    
    def create_assistant(self, name, system_prompt):
        """Create a Vapi assistant"""
        try:
            url = f"{self.base_url}/assistant"
            payload = {
                "name": name,
                "model": {
                    "provider": "openai",
                    "model": "gpt-3.5-turbo",
                    "systemPrompt": system_prompt
                },
                "voice": {
                    "provider": "11labs",
                    "voiceId": "pNInz6obpgDQGcFmaJgB"
                },
                "firstMessage": "Hello! This is your voice assistant. How can I help you today?"
            }
            
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            
            result = response.json()
            print(f"Assistant created: {result}")
            return result
            
        except requests.exceptions.RequestException as e:
            print(f"Error creating assistant: {e}")
            raise
    
    def create_phone_number(self, phone_number, assistant_id):
        """Create a phone number and associate it with an assistant"""
        try:
            url = f"{self.base_url}/phone-number"
            payload = {
                "phoneNumber": phone_number,
                "assistantId": assistant_id,
                "name": f"Phone {phone_number}"
            }
            
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            
            result = response.json()
            print(f"Phone number created: {result}")
            return result
            
        except requests.exceptions.RequestException as e:
            print(f"Error creating phone number: {e}")
            raise
    
    def make_call(self, from_phone_id, to_phone_number, assistant_id):
        """Make a call from source to destination using the correct Vapi payload"""
        try:
            url = f"{self.base_url}/call"
            payload = {
                "assistantId": assistant_id,
                "phoneNumberId": from_phone_id,
                "customer": {
                    "number": to_phone_number
                }
            }
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            result = response.json()
            print(f"Call initiated: {result}")
            return result
        except requests.exceptions.RequestException as e:
            print(f"Error making call: {e}")
            raise
    
    def get_assistants(self):
        """Get all assistants"""
        try:
            url = f"{self.base_url}/assistant"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            result = response.json()
            print(f"Assistants: {result}")
            return result
            
        except requests.exceptions.RequestException as e:
            print(f"Error getting assistants: {e}")
            raise
    
    def get_phone_numbers(self):
        """Get all phone numbers"""
        try:
            url = f"{self.base_url}/phone-number"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error getting phone numbers: {e}")
            return None

    def get_calls(self):
        """Get recent calls"""
        try:
            url = f"{self.base_url}/call"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error getting calls: {e}")
            return None 