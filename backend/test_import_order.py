#!/usr/bin/env python3
"""
Test to fix the import issue by ensuring proper initialization order
"""
import sys
import os

# Add backend to path
backend_path = r"C:\Users\AA\desktop\my-ai-textbook\backend"
sys.path.insert(0, backend_path)

def force_clean_imports():
    """Force clean import of all relevant modules in proper order"""
    
    # Remove all related modules from cache
    modules_to_remove = []
    for name, module in list(sys.modules.items()):
        if (name.startswith('config.') or 
            name.startswith('utils') or 
            name.startswith('api.rag') or
            name.startswith('services')):
            modules_to_remove.append(name)
    
    for name in modules_to_remove:
        del sys.modules[name]
    
    print("Cleared module cache...")

def test_settings_isolated():
    """Test settings in isolation"""
    print("Testing settings in isolation...")
    try:
        from config.settings import settings
        print(f"Settings LOG_LEVEL: {settings.LOG_LEVEL}")
        print("Settings loaded successfully!")
        return True
    except Exception as e:
        print(f"Error loading settings: {e}")
        return False

def test_utils_isolated():
    """Test utils in isolation (but after settings)"""
    print("Testing utils in isolation...")
    try:
        # First make sure settings are loaded
        from config.settings import settings
        print(f"Settings loaded, LOG_LEVEL: {settings.LOG_LEVEL}")
        
        # Then try to import utils
        from utils import logger
        print(f"Utils loaded, logger: {logger.name}")
        print("Utils loaded successfully!")
        return True
    except Exception as e:
        print(f"Error loading utils: {e}")
        return False

def test_api_rag():
    """Test the api rag module (which was causing the issue)"""
    print("Testing api.rag...")
    try:
        # Explicit order of imports
        from config.settings import settings
        print(f"Settings: LOG_LEVEL = {settings.LOG_LEVEL}")
        
        from utils import logger
        print(f"Logger loaded: {logger.name}")
        
        # Now try to import the module that was failing
        import api.rag
        print("api.rag loaded successfully!")
        return True
    except Exception as e:
        print(f"Error loading api.rag: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Testing module import in correct order...\n")
    
    force_clean_imports()
    
    print()
    success1 = test_settings_isolated()
    
    print()
    success2 = test_utils_isolated()
    
    print()
    success3 = test_api_rag()
    
    print(f"\nTests completed: {sum([success1, success2, success3])}/3 passed")
    
    if all([success1, success2, success3]):
        print("All imports working correctly!")
    else:
        print("Some imports still failing")