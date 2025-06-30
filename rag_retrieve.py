import chromadb
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

# Load your KB collection
collection = chroma_client.get_collection("property_management_kb")

def retrieve_similar(query, top_k=3):
    # Embed the query
    query_embedding = azure_ef([query])[0]
    # Search ChromaDB for similar vectors
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "metadatas", "distances"]
    )
    print(f"Query: {query}\n{'='*40}")
    for i, (doc, meta, dist) in enumerate(zip(results["documents"][0], results["metadatas"][0], results["distances"][0])):
        print(f"Rank {i+1} | Distance: {dist:.4f}")
        print(f"Text: {doc}")
        print(f"Metadata: {meta}")
        print('-'*40)

if __name__ == "__main__":
    # Example query
    user_query = "The heater is not working."
    retrieve_similar(user_query) 