import chromadb
from chromadb.config import Settings
from config import AZURE_OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT, AZURE_DEPLOYMENT_NAME
from azure_embedding import AzureOpenAIEmbeddingFunction

azure_ef = AzureOpenAIEmbeddingFunction(
    api_key=AZURE_OPENAI_API_KEY,
    endpoint=AZURE_OPENAI_ENDPOINT,
    deployment_name=AZURE_DEPLOYMENT_NAME
)

chroma_client = chromadb.PersistentClient(path="./chroma_kb")
collection = chroma_client.get_or_create_collection(
    name="property_management_kb"
)

def add_conversation_to_kb(conversation_turns):
    # conversation_turns: list of {"role": ..., "message": ...}
    ids = []
    texts = []
    metadatas = []
    for i, turn in enumerate(conversation_turns):
        ids.append(f"new_{i}_{abs(hash(turn['message']))}")
        texts.append(f"{turn['role']}: {turn['message']}")
        metadatas.append({"role": turn["role"]})
    # Compute embeddings using Azure
    embeddings = azure_ef(texts)
    collection.add(
        ids=ids,
        documents=texts,
        metadatas=metadatas,
        embeddings=embeddings
    )
    print(f"Added {len(ids)} new turns to the knowledge base.")

if __name__ == "__main__":
    # Example usage: add a new conversation
    new_conversation = [
        {"role": "Property Manager", "message": "The elevator is stuck on the 3rd floor."},
        {"role": "Maintenance", "message": "I'll check the control panel and reset the system."},
        {"role": "Property Manager", "message": "Thank you, please update me once it's fixed."},
        {"role": "Maintenance", "message": "Will do. Expect an update in 30 minutes."}
    ]
    add_conversation_to_kb(new_conversation) 