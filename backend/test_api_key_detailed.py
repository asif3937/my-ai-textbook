import os
from config.settings import settings

print(f"Environment variable QDRANT_API_KEY: '{os.getenv('QDRANT_API_KEY', 'NOT SET')}'")
print(f"Settings QDRANT_API_KEY: '{settings.QDRANT_API_KEY}'")
print(f"Boolean value: {bool(settings.QDRANT_API_KEY)}")
print(f"Length: {len(settings.QDRANT_API_KEY)}")
print(f"Strip value: '{settings.QDRANT_API_KEY.strip()}'")
print(f"Strip boolean: {bool(settings.QDRANT_API_KEY.strip())}")

# Also check the file directly
with open('.env', 'r') as f:
    content = f.read()
    print("\n.env file content (relevant lines):")
    for line in content.split('\n'):
        if 'QDRANT_API_KEY' in line:
            print(f"  {line}")