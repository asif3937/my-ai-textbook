from services.qdrant_service import QdrantService

print("Creating QdrantService with REST API...")
qdrant_service = QdrantService()

print(f"Using REST API: {qdrant_service.use_rest_api}")

if qdrant_service.use_rest_api:
    print("Testing collections endpoint via REST...")
    # Create a test collection
    success = qdrant_service.create_collection("test_collection", 1024)
    print(f"Collection creation success: {success}")
    
    # Get collections
    # Since we're using REST directly, we need to call the search method which uses get_collections logic
    # Let's just test that we can create and delete a collection
    delete_success = qdrant_service.delete_collection("test_collection")
    print(f"Collection deletion success: {delete_success}")
else:
    print("Using gRPC client")

print("Qdrant service test completed.")