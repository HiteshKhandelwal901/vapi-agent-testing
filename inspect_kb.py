import chromadb

# Use PersistentClient for disk persistence
chroma_client = chromadb.PersistentClient(path="./chroma_kb")

# List all collections
collections = chroma_client.list_collections()
print("Collections:", [c.name for c in collections])

# Load your KB collection
collection = chroma_client.get_collection("property_management_kb")

# Get all documents and embeddings (limit for display)
results = collection.get(include=["documents", "metadatas", "embeddings"], limit=50)
ids = results.get("ids", [])
docs = results.get("documents", []) or []
metas = results.get("metadatas", []) or []
embeds = results.get("embeddings", []) or []
for id_, doc, meta, emb in zip(ids, docs, metas, embeds):
    print(f"ID: {id_}\nText: {doc}\nMetadata: {meta}\nEmbedding (first 5 dims): {emb[:5]} ...\n{'-'*40}") 