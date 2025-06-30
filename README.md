# Vapi Agent Testing - Two Agent System

A Python-based voice agent system using Vapi that demonstrates communication between two specialized AI agents: **Property Manager** and **Maintenance Agent**.

## 🏗️ Architecture

### **Two Specialized Agents:**
1. **👔 Property Manager Agent** - Initiates calls to report maintenance issues
2. **🔧 Maintenance Agent** - Receives calls and provides maintenance solutions

### **Features:**
- **LLM Integration**: Both agents connected to OpenAI GPT-3.5-turbo
- **Voice Synthesis**: 11labs voice synthesis for natural speech
- **30-Second Calls**: Automated call duration with professional endings
- **Specialized Prompts**: Role-specific system prompts for each agent
- **Phone Number Association**: Each agent has its own dedicated phone number

## 📞 Phone Numbers

- **Property Manager**: `+1 (828) 382-7926` (initiates calls)
- **Maintenance Agent**: `+1 (657) 667-8043` (receives calls)

## 🚀 Quick Start

### 1. **Setup the Two Agents**
```bash
python setup_two_agents.py setup
```

### 2. **Test the Conversation**
```bash
python setup_two_agents.py test
```

### 3. **Simulate the Conversation**
```bash
python simulate_agent_conversation.py
```

## 📋 Agent Roles

### **Property Manager Agent**
- Greets maintenance agent professionally
- Reports property issues that need attention
- Provides specific details about problems
- Asks for estimated completion times
- Ends calls after 30 seconds politely

### **Maintenance Agent**
- Answers calls professionally from property managers
- Listens to reported issues carefully
- Asks clarifying questions about problems
- Provides realistic time estimates for repairs
- Confirms understanding of work needed
- Ends calls after 30 seconds politely

## 🔧 Configuration

### **API Keys**
- **All API keys and secrets must be set in a `.env` file or as environment variables.**
- **Do not put secrets in code or in the README.**

### **AI Models**
- **LLM**: OpenAI GPT-3.5-turbo
- **Voice**: 11labs (Voice ID: pNInz6obpgDQGcFmaJgB)
- **Speech-to-Text**: Deepgram Nova-2

## 📁 Project Structure

```
vapi-agent-testing/
├── config.py                      # Configuration and prompts
├── vapi_agent.py                  # Vapi API client
├── setup_two_agents.py            # Setup and test two agents
├── simulate_agent_conversation.py # Conversation simulation
├── check_calls.py                 # Check call history
├── get_call_details.py            # Get detailed call info
├── app.py                         # Flask web application
└── requirements.txt               # Python dependencies
```

## 🎯 Example Conversation Flow

```
[0s]  👔 Property Manager: "Hello, this is the Property Manager. I need to report some maintenance issues."
[3s]  🔧 Maintenance Agent: "Good morning! I'm the Maintenance Agent. What issues do you have for me today?"
[6s]  👔 Property Manager: "We have a leaking faucet in unit 3B and the HVAC system in the lobby is making strange noises."
[9s]  🔧 Maintenance Agent: "I understand. Can you tell me more about the faucet leak - is it a steady drip or more severe?"
[12s] 👔 Property Manager: "It's a steady drip that's been going on for about two days. The tenant is concerned about water damage."
[15s] 🔧 Maintenance Agent: "Got it. For the faucet, I can have someone there within 2 hours. The HVAC will need a full inspection."
[18s] 👔 Property Manager: "That sounds good. How long do you think the HVAC inspection will take?"
[21s] 🔧 Maintenance Agent: "The HVAC inspection should take about 3-4 hours. I'll schedule it for tomorrow morning."
[24s] 👔 Property Manager: "Perfect. Thank you for your quick response. I'll inform the tenant about the timeline."
[27s] 🔧 Maintenance Agent: "You're welcome. I'll send you a confirmation once the work is scheduled. Have a great day!"
[30s] 📞 Call ends
```

## 📊 Call Analytics

### **Recent Test Results:**
- **Call Duration**: ~33 seconds
- **Cost**: $0.0341
- **Status**: Successfully completed
- **Recording**: Available in Vapi dashboard
- **Transcript**: AI greeting and conversation

## 🔍 Monitoring

### **Check Call Status:**
```bash
python check_calls.py
```

### **Get Detailed Call Info:**
```bash
python get_call_details.py
```

### **Vapi Dashboard:**
- Visit: https://console.vapi.ai
- View call recordings, transcripts, and analytics

## 🛠️ Development

### **Adding New Agents:**
1. Update `config.py` with new agent prompts
2. Add phone numbers to Vapi account
3. Modify `setup_two_agents.py` for new agent setup
4. Test with `python setup_two_agents.py test`

### **Customizing Prompts:**
Edit the system prompts in `config.py`:
- `PROPERTY_MANAGER_PROMPT`
- `MAINTENANCE_AGENT_PROMPT`

## 📈 Future Enhancements

- **Webhook Integration**: Real-time call event handling
- **Database Storage**: Call history and analytics
- **Multi-Agent Scenarios**: More complex conversation flows
- **Custom Voice Models**: Specialized voices for each agent
- **SMS Integration**: Text message notifications

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

---

**Repository**: https://github.com/HiteshKhandelwal901/vapi-agent-testing 