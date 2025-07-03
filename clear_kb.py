import chromadb
import shutil
import os

print("🗑️ Clearing knowledge base...")

# Delete the entire ChromaDB directory
if os.path.exists("./chroma_kb"):
    shutil.rmtree("./chroma_kb")
    print("✅ ChromaDB directory deleted")

# Create a fresh ChromaDB client
chroma_client = chromadb.PersistentClient(path="./chroma_kb")
collection = chroma_client.create_collection(name="property_management_kb")

print("✅ Knowledge base cleared and fresh collection created")
print("📊 Collection count:", len(chroma_client.list_collections())) 