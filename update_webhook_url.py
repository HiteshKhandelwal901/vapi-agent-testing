#!/usr/bin/env python3
"""
Update assistant webhook URL programmatically
"""

from dotenv import load_dotenv
load_dotenv()

from vapi_agent import VapiAgent
import requests

def get_ngrok_url():
    """Get the current ngrok public URL"""
    try:
        response = requests.get('http://localhost:4040/api/tunnels')
        tunnels = response.json()['tunnels']
        
        for tunnel in tunnels:
            if tunnel['config']['addr'] == 'http://localhost:5000':
                public_url = tunnel['public_url']
                # Use https URL
                if public_url.startswith('http://'):
                    public_url = public_url.replace('http://', 'https://')
                return public_url
        
        print("❌ No tunnel found for localhost:5000")
        return None
        
    except Exception as e:
        print(f"❌ Error getting ngrok URL: {e}")
        return None

def update_assistant_webhook():
    """Update all Property Manager assistants with current webhook URL"""
    
    # Get current ngrok URL
    ngrok_url = get_ngrok_url()
    if not ngrok_url:
        print("❌ Could not get ngrok URL. Make sure ngrok is running.")
        return
    
    webhook_url = f"{ngrok_url}/webhook"
    print(f"🔗 Current ngrok URL: {ngrok_url}")
    print(f"🔗 Webhook URL: {webhook_url}")
    
    vapi = VapiAgent()
    
    try:
        # Get all assistants
        print("\n📋 Getting all assistants...")
        assistants = vapi.get_assistants()
        
        if not assistants:
            print("❌ No assistants found")
            return
        
        # Find all assistants (since you deleted from dashboard, we'll update any that exist)
        print(f"\n🎯 Found {len(assistants)} assistant(s)")
        
        # Update webhook URL for each assistant
        for assistant in assistants:
            assistant_id = assistant['id']
            assistant_name = assistant['name']
            current_url = assistant.get('serverUrl', 'Not set')
            
            print(f"\n👔 Updating assistant: {assistant_name}")
            print(f"   ID: {assistant_id}")
            print(f"   Current URL: {current_url}")
            print(f"   New URL: {webhook_url}")
            
            # Update the assistant
            result = vapi.update_assistant_server_url(assistant_id, webhook_url)
            
            if result:
                print(f"   ✅ Successfully updated webhook URL")
            else:
                print(f"   ❌ Failed to update webhook URL")
        
        print(f"\n🎉 Webhook URL update completed!")
        print(f"🔗 All assistants now use: {webhook_url}")
        
    except Exception as e:
        print(f"❌ Error updating webhook URL: {e}")

if __name__ == "__main__":
    print("🔧 Updating Assistant Webhook URLs")
    print("=" * 50)
    update_assistant_webhook() 