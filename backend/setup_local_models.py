#!/usr/bin/env python
"""
Setup script to configure your RAG chatbot to use local models
"""
import os

def configure_local_models():
    """
    Update the .env file to use local models instead of API-based models
    """
    print("Configuring your RAG chatbot to use local models...")
    
    # Read the current .env file
    with open('.env', 'r') as f:
        lines = f.readlines()
    
    # Update the settings to use local models
    updated_lines = []
    for line in lines:
        if line.startswith('LANGUAGE_MODEL_PROVIDER='):
            updated_lines.append('LANGUAGE_MODEL_PROVIDER=local  # Using local models instead of API\n')
        elif line.startswith('LLM_MODEL='):
            updated_lines.append('LLM_MODEL=microsoft/DialoGPT-small  # Local model\n')
        else:
            updated_lines.append(line)
    
    # Write the updated content back to the file
    with open('.env', 'w') as f:
        f.writelines(updated_lines)
    
    print("✅ Configuration updated to use local models")
    print("Now your RAG chatbot will use local models instead of API-based models")
    print("This should resolve the 'fallback mode' issue you were experiencing")
    
    print("\nTo fully benefit from local models, you may want to install these packages:")
    print("pip install transformers torch sentence-transformers")


if __name__ == "__main__":
    configure_local_models()