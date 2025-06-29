#!/usr/bin/env python3
"""
Simulate conversation between Property Manager and Maintenance agents
"""

import time
from datetime import datetime

def simulate_agent_conversation():
    """Simulate a 30-second conversation between the two agents"""
    
    print("🏢 PROPERTY MANAGER ↔️ MAINTENANCE AGENT CONVERSATION")
    print("=" * 60)
    print(f"⏰ Start Time: {datetime.now().strftime('%H:%M:%S')}")
    print("⏱️ Duration: 30 seconds")
    print("=" * 60)
    
    # Conversation flow
    conversation = [
        {
            "speaker": "👔 Property Manager",
            "message": "Hello, this is the Property Manager. I need to report some maintenance issues.",
            "time": 0
        },
        {
            "speaker": "🔧 Maintenance Agent", 
            "message": "Good morning! I'm the Maintenance Agent. What issues do you have for me today?",
            "time": 3
        },
        {
            "speaker": "👔 Property Manager",
            "message": "We have a leaking faucet in unit 3B and the HVAC system in the lobby is making strange noises.",
            "time": 6
        },
        {
            "speaker": "🔧 Maintenance Agent",
            "message": "I understand. Can you tell me more about the faucet leak - is it a steady drip or more severe?",
            "time": 9
        },
        {
            "speaker": "👔 Property Manager",
            "message": "It's a steady drip that's been going on for about two days. The tenant is concerned about water damage.",
            "time": 12
        },
        {
            "speaker": "🔧 Maintenance Agent",
            "message": "Got it. For the faucet, I can have someone there within 2 hours. The HVAC will need a full inspection.",
            "time": 15
        },
        {
            "speaker": "👔 Property Manager",
            "message": "That sounds good. How long do you think the HVAC inspection will take?",
            "time": 18
        },
        {
            "speaker": "🔧 Maintenance Agent",
            "message": "The HVAC inspection should take about 3-4 hours. I'll schedule it for tomorrow morning.",
            "time": 21
        },
        {
            "speaker": "👔 Property Manager",
            "message": "Perfect. Thank you for your quick response. I'll inform the tenant about the timeline.",
            "time": 24
        },
        {
            "speaker": "🔧 Maintenance Agent",
            "message": "You're welcome. I'll send you a confirmation once the work is scheduled. Have a great day!",
            "time": 27
        }
    ]
    
    start_time = time.time()
    
    for exchange in conversation:
        # Wait until the appropriate time
        elapsed = time.time() - start_time
        if elapsed < exchange["time"]:
            time.sleep(exchange["time"] - elapsed)
        
        current_time = time.time() - start_time
        print(f"\n[{current_time:.1f}s] {exchange['speaker']}:")
        print(f"   {exchange['message']}")
        
        # Check if we've reached 30 seconds
        if current_time >= 30:
            break
    
    print("\n" + "=" * 60)
    print(f"⏰ End Time: {datetime.now().strftime('%H:%M:%S')}")
    print("📞 Call ended after 30 seconds")
    print("✅ Conversation completed successfully!")
    print("\n🎯 Key Features Demonstrated:")
    print("   • Professional greeting and role identification")
    print("   • Issue reporting and clarification")
    print("   • Time estimates and scheduling")
    print("   • Professional call ending")
    print("   • 30-second duration limit")

if __name__ == "__main__":
    simulate_agent_conversation() 