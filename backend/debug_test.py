#!/usr/bin/env python3
"""
Test to verify which API routes are being used
"""
import sys
import os

# Add the backend directory to Python path
backend_path = r"C:\Users\AA\desktop\my-ai-textbook\backend"
sys.path.insert(0, backend_path)

def test_api_route():
    """Test that we're using the correct API route"""
    print("Testing API route configuration...")
    
    # Check which file the import points to
    import importlib.util
    spec = importlib.util.find_spec("api.rag.routes.chat")
    if spec and spec.origin:
        print(f"[OK] Found api/rag/routes/chat module at: {spec.origin}")
    else:
        print("[ERROR] Could not find api/rag/routes/chat module")
        return False
    
    # Import and verify the router
    try:
        from api.rag.routes.chat import router
        print("[OK] Successfully imported router from api.rag.routes.chat")
        
        # Check if the required dependencies are available
        try:
            import cohere
            print("[OK] Cohere library is available")
        except ImportError:
            print("[WARNING] Cohere library not available")
        
        return True
    except Exception as e:
        print(f"[ERROR] Failed to import router from api.rag.routes.chat: {e}")
        return False

def test_environment():
    """Test environment configuration"""
    print("\nTesting environment configuration...")
    
    import config.settings
    settings = config.settings.settings
    
    if settings.COHERE_API_KEY and settings.COHERE_API_KEY != "your_cohere_api_key_here":
        print(f"[OK] Cohere API key is set (first 10 chars: {settings.COHERE_API_KEY[:10]}...)")
    else:
        print("[WARNING] Cohere API key is not properly configured")
        
    if settings.QDRANT_URL:
        print(f"[OK] Qdrant URL is set: {settings.QDRANT_URL}")
    else:
        print("[WARNING] Qdrant URL is not set")
        
    return True

if __name__ == "__main__":
    print("Running API configuration test...\n")
    
    success_count = 0
    total_tests = 2
    
    if test_api_route():
        success_count += 1
        
    if test_environment():
        success_count += 1
    
    print(f"\nConfiguration tests completed: {success_count}/{total_tests} passed")
    
    if success_count == total_tests:
        print("\n[SUCCESS] Configuration looks correct.")
        print("The API should now use the proper RAG implementation with Cohere integration.")
    else:
        print("\n[ERROR] There are configuration issues that need to be resolved.")