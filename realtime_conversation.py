#!/usr/bin/env python3
"""
Real-time conversation monitor for VAPI calls
"""

import requests
import json
import time
from datetime import datetime
import threading

class ConversationMonitor:
    def __init__(self):
        self.conversation_history = []
        self.call_start_time = None
        self.is_monitoring = False
        
    def start_monitoring(self, call_id):
        """Start monitoring conversation for a specific call"""
        self.call_id = call_id
        self.call_start_time = datetime.now()
        self.is_monitoring = True
        
        print("🎯 REAL-TIME CONVERSATION MONITOR")
        print("=" * 60)
        print(f"📞 Call ID: {call_id}")
        print(f"📱 Destination: +918660186104")
        print(f"⏰ Start time: {self.call_start_time.strftime('%H:%M:%S')}")
        print("=" * 60)
        print("💬 CONVERSATION LOG:")
        print("=" * 60)
        
        # Start monitoring thread
        monitor_thread = threading.Thread(target=self._monitor_webhook)
        monitor_thread.daemon = True
        monitor_thread.start()
        
        return monitor_thread
    
    def _monitor_webhook(self):
        """Monitor webhook for conversation data"""
        while self.is_monitoring:
            try:
                # Check for new conversation data
                time.sleep(1)
            except KeyboardInterrupt:
                break
    
    def add_conversation_turn(self, role, message, timestamp=None):
        """Add a conversation turn to the log"""
        if not timestamp:
            timestamp = datetime.now()
        
        turn = {
            "role": role,
            "message": message,
            "timestamp": timestamp
        }
        
        self.conversation_history.append(turn)
        
        # Print in real-time
        role_emoji = "🤖" if role.lower() in ["ai", "bot", "assistant"] else "👤"
        time_str = timestamp.strftime('%H:%M:%S')
        
        print(f"\n{role_emoji} [{time_str}] {role.upper()}:")
        print(f"   {message}")
        print("-" * 40)
    
    def stop_monitoring(self):
        """Stop monitoring"""
        self.is_monitoring = False
        print("\n🛑 Conversation monitoring stopped")
        print(f"📊 Total turns: {len(self.conversation_history)}")
        print("=" * 60)

# Global monitor instance
monitor = ConversationMonitor()

def start_conversation_monitor(call_id):
    """Start monitoring conversation for a call"""
    return monitor.start_monitoring(call_id)

def add_turn(role, message):
    """Add a conversation turn"""
    monitor.add_conversation_turn(role, message)

def stop_monitor():
    """Stop the monitor"""
    monitor.stop_monitoring() 