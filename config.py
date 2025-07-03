import os

# Vapi Configuration
VAPI_PRIVATE_KEY = os.environ.get("VAPI_PRIVATE_KEY")
VAPI_PUBLIC_KEY = os.environ.get("VAPI_PUBLIC_KEY")

# OpenAI API Key for embeddings (not used for Azure)
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# Azure OpenAI config for embeddings
AZURE_DEPLOYMENT_NAME = os.environ.get("AZURE_DEPLOYMENT_NAME")
AZURE_OPENAI_API_KEY = os.environ.get("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.environ.get("AZURE_OPENAI_ENDPOINT")

# Chat completions (GPT)
AZURE_OPENAI_GPT_API_KEY2 = os.environ.get("AZURE_OPENAI_GPT_API_KEY2")
AZURE_OPENAI_GPT_ENDPOINT2 = os.environ.get("AZURE_OPENAI_GPT_ENDPOINT2")
AZURE_GPT_DEPLOYMENT_NAME2 = os.environ.get("AZURE_GPT_DEPLOYMENT_NAME2")

# Phone Numbers (you'll need to add these to your Vapi account)
PROPERTY_MANAGER_PHONE = os.environ.get("PROPERTY_MANAGER_PHONE")  # Existing source number
MAINTENANCE_PHONE = os.environ.get("MAINTENANCE_PHONE")           # Existing destination number

# API Configuration
VAPI_BASE_URL = "https://api.vapi.ai"

# Webhook/Server URL for assistant events (set this to your public URL)
SERVER_URL = os.environ.get("SERVER_URL")  # <-- Set this!

# Agent Configuration
PROPERTY_MANAGER_PROMPT = """You are a Property Manager agent who is going to call maintaince person based on miantiance complaints recieved from tenants. For exanoe if tenant compalaints AC issue, you are going to call the maintaince guy and explian the issue and chek for his vailablity.from tean Your role is to:
 Your role is to:
1. Greet the maintenance person with warm message 
2. Report property issues that needs attention
3. Provide specific details about the problems
4. Ask for estimated completion time and starting time and availability. 


Keep responses brief, professional, and focused on property management tasks."""

MAINTENANCE_AGENT_PROMPT = """You are a Maintenance Agent. Your role is to:
1. Answer calls professionally from property managers
2. Listen to reported issues carefully
3. Ask clarifying questions about the problems
4. Provide realistic time estimates for repairs
5. Confirm understanding of the work needed
6. End the call after 30 seconds politely

Keep responses brief, professional, and focused on maintenance tasks."""

# NOTE: Set all secret keys and phone numbers in a .env file or as environment variables. 