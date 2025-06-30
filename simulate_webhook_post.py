import requests

WEBHOOK_URL = "http://localhost:5000/webhook"

payload = {
    "call_id": "sim_test_001",
    "transcript": [
        {"role": "Property Manager", "text": "Hello, this is the property manager. How can I help you?"},
        {"role": "Tenant", "text": "Hi, the heater in my apartment is not working."},
        {"role": "Property Manager", "text": "I'll send the HVAC technician to check it out."}
    ]
}

response = requests.post(WEBHOOK_URL, json=payload)
print(f"Status code: {response.status_code}")
print(f"Response: {response.text}") 