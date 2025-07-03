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
    
    def create_assistant(self, name, system_prompt, server_url=None):
        """Create a Vapi assistant, optionally setting the serverUrl (webhook)"""
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
                "firstMessage": "Hello! I'm Honey, calling from ABC property management firm regarding a maintinace fix request. Is this good time to talk?"
            }
            if server_url:
                payload["serverUrl"] = server_url
            # Debug print statements
            print("[DEBUG] Vapi create_assistant request:")
            print("URL:", url)
            print("Headers:", self.headers)
            print("Payload:", json.dumps(payload, indent=2))
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            result = response.json()
            print(f"Assistant created: {result}")
            return result
        except requests.exceptions.RequestException as e:
            print(f"Error creating assistant: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print("[DEBUG] Response status:", e.response.status_code)
                print("[DEBUG] Response body:", e.response.text)
            raise

    def update_assistant_server_url(self, assistant_id, server_url):
        """Update the serverUrl (webhook) for an existing assistant"""
        try:
            url = f"{self.base_url}/assistant/{assistant_id}"
            payload = {"serverUrl": server_url}
            response = requests.patch(url, headers=self.headers, json=payload)
            response.raise_for_status()
            result = response.json()
            print(f"Assistant serverUrl updated: {result}")
            return result
        except requests.exceptions.RequestException as e:
            print(f"Error updating assistant serverUrl: {e}")
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
            print("[DEBUG] Vapi make_call request:")
            print("URL:", url)
            print("Headers:", self.headers)
            print("Payload:", json.dumps(payload, indent=2))
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            result = response.json()
            print(f"Call initiated: {result}")
            return result
        except requests.exceptions.RequestException as e:
            print(f"Error making call: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print("[DEBUG] Response status:", e.response.status_code)
                print("[DEBUG] Response body:", e.response.text)
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

    def update_phone_number(self, phone_id, assistant_id, name):
        """Update a phone number to associate it with an assistant"""
        try:
            url = f"{self.base_url}/phone-number/{phone_id}"
            payload = {
                "assistantId": assistant_id,
                "name": name
            }
            response = requests.patch(url, headers=self.headers, json=payload)
            response.raise_for_status()
            result = response.json()
            print(f"Phone number updated: {result}")
            return result
        except requests.exceptions.RequestException as e:
            print(f"Error updating phone number: {e}")
            raise 