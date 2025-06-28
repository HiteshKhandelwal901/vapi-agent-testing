#!/usr/bin/env python3
"""
Test simulation for Vapi voice agent
This simulates the conversation flow without making actual calls
"""

def simulate_conversation():
    """Simulate a conversation between the voice agent and a user"""
    
    print("🎯 VAPI VOICE AGENT TEST SIMULATION")
    print("=" * 50)
    
    # Simulate the call being initiated
    print("📞 Call initiated from +18283827926 to +16576678043")
    print("🤖 Voice Agent: Hello! This is your voice assistant. How can I help you today?")
    
    # Simulate user responses
    user_responses = [
        "Hi! I'd like to test this voice agent.",
        "Can you tell me about your capabilities?",
        "That sounds great, thank you!"
    ]
    
    agent_responses = [
        "I understand your request. Let me assist you with that.",
        "I can help with various tasks, answer questions, and provide information. What would you like to know?",
        "Thank you for the conversation. Have a great day!"
    ]
    
    for i, (user_msg, agent_msg) in enumerate(zip(user_responses, agent_responses)):
        print(f"\n👤 User: {user_msg}")
        print(f"🤖 Voice Agent: {agent_msg}")
        
        if i == 2:  # After 3 exchanges
            print("\n📞 Call ended after 3 exchanges")
            break
    
    print("\n✅ Simulation completed!")
    print("\nTo test with real calls:")
    print("1. Update DESTINATION_PHONE_NUMBER in config.py with your phone number")
    print("2. Run: python setup.py test")

if __name__ == "__main__":
    simulate_conversation() 