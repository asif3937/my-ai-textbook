from qdrant_client import QdrantClient

# Test direct connection
try:
    print("Testing direct Qdrant connection...")
    client = QdrantClient(url="http://localhost:6333", prefer_grpc=False)
    
    # Try to get collections
    collections = client.get_collections()
    print("Connection successful!")
    print(f"Found {len(collections.collections)} collections")
    for collection in collections.collections:
        print(f"  - {collection.name}")
except Exception as e:
    print(f"Connection failed: {e}")