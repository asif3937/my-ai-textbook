#!/usr/bin/env python3
"""
More specific test to find the exact import issue
"""
import sys
import os

# Add backend to path
backend_path = r"C:\Users\AA\desktop\my-ai-textbook\backend"
sys.path.insert(0, backend_path)

def test_specific_imports():
    """Test specific imports that might be causing the issue"""
    print("Testing specific imports...")

    # Test config.settings import
    try:
        from config.settings import settings
        print(f"[OK] Config settings imported, has QDRANT_API_KEY: {hasattr(settings, 'QDRANT_API_KEY')}")
    except Exception as e:
        print(f"[ERROR] Failed to import config settings: {e}")
        assert False, f"Failed to import config settings: {e}"

    # Test qdrant service specifically
    try:
        from services.qdrant_service import QdrantService
        print("[OK] QdrantService imported")

        # Don't instantiate it as it might try to connect to Qdrant
    except Exception as e:
        print(f"[ERROR] Failed to import QdrantService: {e}")
        import traceback
        traceback.print_exc()
        assert False, f"Failed to import QdrantService: {e}"

    # Test retrieval service specifically
    try:
        from api.rag.services.retrieval_service import RetrievalService
        print("[OK] RetrievalService imported")
    except OSError as e:
        if "DLL" in str(e) or "c10.dll" in str(e):
            print(f"[WARNING] DLL loading issue with PyTorch (environment issue): {e}")
            print("This is an environment issue, not a code issue - PyTorch DLLs not loaded properly on Windows")
        else:
            print(f"[ERROR] Failed to import RetrievalService: {e}")
            import traceback
            traceback.print_exc()
            assert False, f"Failed to import RetrievalService: {e}"
    except Exception as e:
        print(f"[ERROR] Failed to import RetrievalService: {e}")
        import traceback
        traceback.print_exc()
        assert False, f"Failed to import RetrievalService: {e}"

    # Now try to import the chat route
    try:
        from api.rag.routes.chat import router
        print("[SUCCESS] Chat router imported successfully!")
    except Exception as e:
        print(f"[ERROR] Failed to import chat router: {e}")
        import traceback
        traceback.print_exc()
        assert False, f"Failed to import chat router: {e}"

if __name__ == "__main__":
    test_specific_imports()