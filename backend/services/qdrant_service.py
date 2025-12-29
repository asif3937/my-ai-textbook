import uuid
from typing import List, Optional, Dict, Any
from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import Distance, VectorParams
from config.settings import settings
import requests
import json


class QdrantService:
    def __init__(self):
        # Initialize Qdrant client
        if settings.QDRANT_API_KEY and settings.QDRANT_API_KEY.strip():
            # Using cloud instance with API key
            self.client = QdrantClient(
                url=settings.QDRANT_URL,
                api_key=settings.QDRANT_API_KEY,
                prefer_grpc=True
            )
            self.use_rest_api = False
        else:
            # For local instance, use REST API directly to avoid gRPC issues
            self.qdrant_url = "http://localhost:6333"
            self.use_rest_api = True
            # Initialize a dummy client just for type compatibility
            # We'll use REST API directly
            self.client = None

    def create_collection(self, collection_name: str, vector_size: int = 1536):
        """Create a collection to store embeddings"""
        if self.use_rest_api:
            # Use REST API directly
            url = f"{self.qdrant_url}/collections/{collection_name}"
            
            payload = {
                "vectors": {
                    "size": vector_size,
                    "distance": "Cosine"
                }
            }
            
            try:
                response = requests.put(url, json=payload)
                if response.status_code == 200:
                    return True
                else:
                    print(f"Error creating collection {collection_name}: {response.text}")
                    return False
            except Exception as e:
                print(f"Error creating collection {collection_name}: {e}")
                return False
        else:
            # Use gRPC client
            try:
                self.client.create_collection(
                    collection_name=collection_name,
                    vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
                )
                return True
            except Exception as e:
                print(f"Error creating collection {collection_name}: {e}")
                return False

    def delete_collection(self, collection_name: str):
        """Delete a collection"""
        if self.use_rest_api:
            # Use REST API directly
            url = f"{self.qdrant_url}/collections/{collection_name}"
            
            try:
                response = requests.delete(url)
                if response.status_code == 200:
                    return True
                else:
                    print(f"Error deleting collection {collection_name}: {response.text}")
                    return False
            except Exception as e:
                print(f"Error deleting collection {collection_name}: {e}")
                return False
        else:
            # Use gRPC client
            try:
                self.client.delete_collection(collection_name)
                return True
            except Exception as e:
                print(f"Error deleting collection {collection_name}: {e}")
                return False

    def upsert_vectors(
        self,
        collection_name: str,
        vectors: List[List[float]],
        payloads: List[Dict[str, Any]],
        ids: Optional[List[str]] = None
    ):
        """Upsert vectors into a collection"""
        if ids is None:
            ids = [str(uuid.uuid4()) for _ in vectors]

        if self.use_rest_api:
            # Use REST API directly
            url = f"{self.qdrant_url}/collections/{collection_name}/points"
            
            points = []
            for i, (vector, payload) in enumerate(zip(vectors, payloads)):
                point = {
                    "id": ids[i],
                    "vector": vector,
                    "payload": payload
                }
                points.append(point)
            
            payload = {
                "points": points
            }
            
            try:
                response = requests.put(url, json=payload)
                if response.status_code == 200:
                    return ids
                else:
                    print(f"Error upserting vectors to {collection_name}: {response.text}")
                    return []
            except Exception as e:
                print(f"Error upserting vectors to {collection_name}: {e}")
                return []
        else:
            # Use gRPC client
            try:
                self.client.upsert(
                    collection_name=collection_name,
                    points=models.Batch(
                        ids=ids,
                        vectors=vectors,
                        payloads=payloads
                    )
                )
                return ids
            except Exception as e:
                print(f"Error upserting vectors to {collection_name}: {e}")
                return []

    def search_vectors(
        self,
        collection_name: str,
        query_vector: List[float],
        limit: int = 10,
        filters: Optional[Dict[str, Any]] = None
    ):
        """Search for similar vectors in the collection"""
        if self.use_rest_api:
            # Use REST API directly
            url = f"{self.qdrant_url}/collections/{collection_name}/points/search"
            
            payload = {
                "vector": query_vector,
                "limit": limit
            }
            
            if filters:
                # Convert filters to Qdrant REST format
                filter_conditions = []
                for key, value in filters.items():
                    filter_conditions.append({
                        "key": key,
                        "match": {"value": value}
                    })
                
                if filter_conditions:
                    payload["filter"] = {"must": filter_conditions}
            
            try:
                response = requests.post(url, json=payload)
                if response.status_code == 200:
                    results = response.json()["result"]
                    # Convert to the same format as gRPC response
                    formatted_results = []
                    for result in results:
                        formatted_result = type('obj', (object,), {
                            'id': result['id'],
                            'score': result['score'],
                            'payload': result.get('payload', {}),
                        })()
                        formatted_results.append(formatted_result)
                    return formatted_results
                else:
                    print(f"Error searching vectors in {collection_name}: {response.text}")
                    return []
            except Exception as e:
                print(f"Error searching vectors in {collection_name}: {e}")
                return []
        else:
            # Use gRPC client
            try:
                # Convert filters to Qdrant format if provided
                qdrant_filters = None
                if filters:
                    conditions = []
                    for key, value in filters.items():
                        conditions.append(
                            models.FieldCondition(
                                key=key,
                                match=models.MatchValue(value=value)
                            )
                        )
                    if conditions:
                        qdrant_filters = models.Filter(must=conditions)

                results = self.client.search(
                    collection_name=collection_name,
                    query_vector=query_vector,
                    limit=limit,
                    query_filter=qdrant_filters,
                    with_payload=True
                )

                return results
            except Exception as e:
                print(f"Error searching vectors in {collection_name}: {e}")
                return []

    def get_vectors_by_ids(self, collection_name: str, ids: List[str]):
        """Get vectors by their IDs"""
        if self.use_rest_api:
            # Use REST API directly
            url = f"{self.qdrant_url}/collections/{collection_name}/points"
            
            # Format IDs as a comma-separated string
            ids_str = ','.join(ids)
            params = {'ids': ids_str}
            
            try:
                response = requests.get(url, params=params)
                if response.status_code == 200:
                    results = response.json()["result"]
                    # Convert to the same format as gRPC response
                    formatted_results = []
                    for result in results:
                        formatted_result = type('obj', (object,), {
                            'id': result['id'],
                            'vector': result['vector'],
                            'payload': result.get('payload', {}),
                        })()
                        formatted_results.append(formatted_result)
                    return formatted_results
                else:
                    print(f"Error retrieving vectors by IDs from {collection_name}: {response.text}")
                    return []
            except Exception as e:
                print(f"Error retrieving vectors by IDs from {collection_name}: {e}")
                return []
        else:
            # Use gRPC client
            try:
                results = self.client.retrieve(
                    collection_name=collection_name,
                    ids=ids
                )
                return results
            except Exception as e:
                print(f"Error retrieving vectors by IDs from {collection_name}: {e}")
                return []

    def delete_vectors_by_ids(self, collection_name: str, ids: List[str]):
        """Delete vectors by their IDs"""
        if self.use_rest_api:
            # Use REST API directly
            url = f"{self.qdrant_url}/collections/{collection_name}/points/delete"
            
            payload = {
                "points": ids
            }
            
            try:
                response = requests.post(url, json=payload)
                if response.status_code == 200:
                    return True
                else:
                    print(f"Error deleting vectors by IDs from {collection_name}: {response.text}")
                    return False
            except Exception as e:
                print(f"Error deleting vectors by IDs from {collection_name}: {e}")
                return False
        else:
            # Use gRPC client
            try:
                self.client.delete(
                    collection_name=collection_name,
                    points_selector=models.PointIdsList(
                        points=ids
                    )
                )
                return True
            except Exception as e:
                print(f"Error deleting vectors by IDs from {collection_name}: {e}")
                return False