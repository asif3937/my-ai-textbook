from qdrant_client import QdrantClient

# Test various connection methods
try:
    print("Testing Qdrant connection method 1: host and port")
    client1 = QdrantClient(host="localhost", port=6333, prefer_grpc=False)
    collections = client1.get_collections()
    print("Method 1 successful!")
    print(f"Found {len(collections.collections)} collections")
except Exception as e:
    print(f"Method 1 failed: {e}")

try:
    print("\nTesting Qdrant connection method 2: URL with http:// prefix")
    client2 = QdrantClient(url="http://localhost:6333", prefer_grpc=False)
    collections = client2.get_collections()
    print("Method 2 successful!")
    print(f"Found {len(collections.collections)} collections")
except Exception as e:
    print(f"Method 2 failed: {e}")

try:
    print("\nTesting Qdrant connection method 3: without prefer_grpc parameter")
    client3 = QdrantClient(host="localhost", port=6333)
    collections = client3.get_collections()
    print("Method 3 successful!")
    print(f"Found {len(collections.collections)} collections")
except Exception as e:
    print(f"Method 3 failed: {e}")