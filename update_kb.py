import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key=openai.api_key,
    model_name="text-embedding-3-small"
)

chroma_client = chromadb.Client(Settings(persist_directory="./chroma_kb"))
collection = chroma_client.get_or_create_collection(
    name="property_management_kb",
    embedding_function=openai_ef
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
    collection.add(
        ids=ids,
        documents=texts,
        metadatas=metadatas
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