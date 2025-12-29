from services.qdrant_service import QdrantService

print("Creating QdrantService...")
qdrant_service = QdrantService()
print("QdrantService created without connecting")

print("Now getting the client...")
client = qdrant_service._ensure_client()
print("Client obtained")

print("Testing collections...")
collections = client.get_collections()
print(f"Success! Found {len(collections.collections)} collections")