#!/usr/bin/env python3
"""
Test the full app import to identify the issue
"""
import sys
import os

# Add backend to path
backend_path = r"C:\Users\AA\desktop\my-ai-textbook\backend"
sys.path.insert(0, backend_path)

def test_full_import():
    """Test importing the main app"""
    try:
        from main import app
        print("[SUCCESS] Main app imported successfully")
    except Exception as e:
        print(f"[ERROR] Failed to import main app: {e}")
        import traceback
        traceback.print_exc()
        assert False, f"Failed to import main app: {e}"

if __name__ == "__main__":
    test_full_import()