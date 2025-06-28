# Vapi Voice Agent

A Python-based voice agent using Vapi that gets triggered based on events. This project demonstrates how to create a single voice agent that can make calls from a source phone number to a destination phone number using Vapi's API.

## Features

- Create a single Vapi voice assistant with custom system prompt
- Set up a source phone number and associate it with the assistant
- Trigger calls from source to destination programmatically
- Handle webhooks for call events
- Simple conversation flow with automatic exit after a few exchanges

## Configuration

The project uses the following configuration:

- **Private Key**: `02907a93-2328-4f9f-8383-f80038571981`
- **Public Key**: `832e23b9-6647-41be-adde-b50bf18224d5`
- **Source Phone**: `+1 (828) 382-7926` (makes the calls)
- **Destination Phone**: `+1 (657) 667-8043` (receives the calls)

## Setup

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Setup the voice agent and phone number**:
   ```bash
   python setup.py setup
   ```

3. **Start the web server**:
   ```bash
   python app.py
   ```

## Usage

### Command Line

- **Setup voice agent and phone number**:
  ```bash
  python setup.py setup
  ```

- **Test a call from source to destination**:
  ```bash
  python setup.py test
  ```

### Web API

The Flask server provides the following endpoints:

- **Health Check**: `GET http://localhost:5000/health`
- **Setup**: `POST http://localhost:5000/setup`
- **Trigger Call**: `POST http://localhost:5000/trigger-call`
- **Webhook**: `POST http://localhost:5000/webhook` (for Vapi callbacks)

### Testing the Voice Agent

1. **Start the server**:
   ```bash
   python app.py
   ```

2. **Setup the agent** (if not done already):
   ```bash
   curl -X POST http://localhost:5000/setup
   ```

3. **Trigger a call**:
   ```bash
   curl -X POST http://localhost:5000/trigger-call
   ```

4. **Check health**:
   ```bash
   curl http://localhost:5000/health
   ```

## Project Structure

```
vapi_testing/
├── requirements.txt      # Python dependencies
├── config.py            # Configuration settings
├── vapi_agent.py        # Vapi API client class
├── setup.py             # Setup script for agent and phone number
├── app.py               # Flask web application
└── README.md            # This file
```

## How It Works

1. **Setup Phase**: Creates a single Vapi voice assistant with a system prompt
2. **Phone Number**: Associates the source phone number with the assistant
3. **Call Trigger**: When triggered, initiates a call from source to destination
4. **Conversation Flow**: 
   - Voice agent greets the destination and asks how it can help
   - After brief conversation, politely ends the call
   - Conversation exits after a few exchanges

## Webhook Configuration

To receive call events from Vapi, configure your webhook URL in the Vapi dashboard:
```
http://your-domain.com/webhook
```

The webhook handles:
- `call-start`: Initializes the conversation
- `call-end`: Cleans up when call ends
- `function-call`: Handles any function calls (if needed)

## Customization

You can customize the voice agent by modifying:

- **System prompt** in `setup.py`
- **Voice settings** in `vapi_agent.py`
- **Conversation flow** in `app.py`
- **Response logic** in the `get_llm_response` function

## Troubleshooting

1. **API Key Issues**: Ensure your Vapi API keys are correct in `config.py`
2. **Phone Number Issues**: Verify phone numbers are properly formatted with country codes
3. **Webhook Issues**: Make sure your webhook URL is publicly accessible
4. **Call Failures**: Check Vapi dashboard for call logs and error messages

## Next Steps

- Integrate with a more sophisticated LLM
- Add conversation state management
- Implement call scheduling
- Add error handling and retry mechanisms
- Create a web interface for managing calls 