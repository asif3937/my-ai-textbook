import os
# Unset the environment variable to force reading from .env file
if 'QDRANT_API_KEY' in os.environ:
    del os.environ['QDRANT_API_KEY']

from services.qdrant_service import QdrantService

print("Creating QdrantService with REST API...")
qdrant_service = QdrantService()

print(f"Using REST API: {qdrant_service.use_rest_api}")

if qdrant_service.use_rest_api:
    print("Testing collections endpoint via REST...")
    # Create a test collection
    success = qdrant_service.create_collection("test_collection", 1024)
    print(f"Collection creation success: {success}")
    
    # Delete the test collection
    delete_success = qdrant_service.delete_collection("test_collection")
    print(f"Collection deletion success: {delete_success}")
    
    print("REST API test completed successfully!")
else:
    print("Using gRPC client - this means the API key was not properly handled")
    
print("Qdrant service test completed.")