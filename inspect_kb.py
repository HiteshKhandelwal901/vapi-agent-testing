import chromadb

# Use PersistentClient for disk persistence (same as Flask app)
chroma_client = chromadb.PersistentClient(path="./chroma_kb")

# List all collections
print("Collections:", chroma_client.list_collections())

# Load your KB collection
collection = chroma_client.get_or_create_collection(
    name="property_management_kb"
)

# Get all documents and embeddings (limit for display)
results = collection.get(include=["documents", "metadatas", "embeddings"], limit=50)
ids = results.get("ids", [])
docs = results.get("documents", []) or []
metas = results.get("metadatas", []) or []
embeds = results.get("embeddings", []) or []
for id_, doc, meta, emb in zip(ids, docs, metas, embeds):
    print(f"ID: {id_}\nText: {doc}\nMetadata: {meta}\nEmbedding (first 5 dims): {emb[:5]} ...\n{'-'*40}")

# Fetch all documents and print their text
results = collection.get()
print("\n--- Conversation Turns in KB ---")
for i, text in enumerate(results.get('documents') or []):
    print(f"Turn {i}: {text}")
print("-------------------------------") 