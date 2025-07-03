import os
from dotenv import load_dotenv
load_dotenv()
import chromadb
from kb_conversations import conversations
from azure_embedding import AzureOpenAIEmbeddingFunction
from config import AZURE_OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT, AZURE_DEPLOYMENT_NAME

# Use PersistentClient for disk persistence
chroma_client = chromadb.PersistentClient(path="./chroma_kb")

# Use Azure OpenAI embedding function
azure_ef = AzureOpenAIEmbeddingFunction(
    api_key=AZURE_OPENAI_API_KEY,
    endpoint=AZURE_OPENAI_ENDPOINT,
    deployment_name=AZURE_DEPLOYMENT_NAME
)

# Create or load ChromaDB collection
collection = chroma_client.get_or_create_collection(
    name="property_management_kb",
    embedding_function=azure_ef
)

def build_kb():
    print("Building knowledge base from simulated conversations...")
    ids = []
    texts = []
    metadatas = []
    for i, turn in enumerate(conversations):
        ids.append(f"turn_{i}")
        texts.append(f"{turn['role']}: {turn['message']}")
        metadatas.append({"role": turn["role"]})
    # Add to ChromaDB
    collection.add(
        ids=ids,
        documents=texts,
        metadatas=metadatas
    )
    print(f"Added {len(ids)} conversation turns to the knowledge base.")

if __name__ == "__main__":
    build_kb() 