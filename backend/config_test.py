#!/usr/bin/env python3
"""
Test script to verify configuration fixes
"""

def test_settings():
    """Test that all settings can be loaded without errors"""
    from config.settings import settings
    print("[OK] Settings class loaded successfully")

    # Test accessing all the variables we've configured
    assert hasattr(settings, 'LOG_LEVEL'), "LOG_LEVEL not found"
    assert hasattr(settings, 'SECRET_KEY'), "SECRET_KEY not found"
    assert hasattr(settings, 'QDRANT_URL'), "QDRANT_URL not found"
    assert hasattr(settings, 'QDRANT_API_KEY'), "QDRANT_API_KEY not found"
    assert hasattr(settings, 'QDRANT_COLLECTION_NAME'), "QDRANT_COLLECTION_NAME not found"
    assert hasattr(settings, 'COHERE_API_KEY'), "COHERE_API_KEY not found"
    assert hasattr(settings, 'OPENAI_API_KEY'), "OPENAI_API_KEY not found"
    assert hasattr(settings, 'EMBEDDING_MODEL'), "EMBEDDING_MODEL not found"
    assert hasattr(settings, 'EMBEDDING_DIMENSION'), "EMBEDDING_DIMENSION not found"

    print(f"[OK] All settings attributes accessible. LOG_LEVEL = {settings.LOG_LEVEL}")
    return True

def test_main_import_without_services():
    """Test that main can be imported without loading heavy services"""
    # We'll temporarily replace problematic imports with mocks
    import sys
    from unittest.mock import Mock

    # Mock the problematic service imports
    sys.modules['sentence_transformers'] = Mock()
    sys.modules['cohere'] = Mock()
    sys.modules['qdrant_client'] = Mock()
    sys.modules['qdrant_client.http'] = Mock()
    sys.modules['qdrant_client.http.models'] = Mock()

    try:
        from main import app
        print("[OK] Main app imported successfully (with mocked services)")
        return True
    except ImportError as e:
        print(f"[ERROR] Failed to import main: {e}")
        return False

def test_models():
    """Test that models can be imported"""
    try:
        from models import BookContent, Session, ContentChunk, ChatHistory
        print("[OK] All models imported successfully")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to import models: {e}")
        return False

if __name__ == "__main__":
    print("Running configuration tests...\n")

    success_count = 0
    total_tests = 3

    if test_settings():
        success_count += 1

    print()  # blank line

    if test_models():
        success_count += 1

    print()  # blank line

    if test_main_import_without_services():
        success_count += 1

    print(f"\nConfiguration tests completed: {success_count}/{total_tests} passed")

    if success_count == total_tests:
        print("[SUCCESS] All configuration fixes successful!")
    else:
        print("[ERROR] Some configuration issues remain")