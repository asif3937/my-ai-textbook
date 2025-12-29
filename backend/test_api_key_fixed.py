import os
# Unset the environment variable to force reading from .env file
if 'QDRANT_API_KEY' in os.environ:
    del os.environ['QDRANT_API_KEY']

from config.settings import settings

print(f"After unsetting - Environment variable QDRANT_API_KEY: '{os.getenv('QDRANT_API_KEY', 'NOT SET')}'")
print(f"After unsetting - Settings QDRANT_API_KEY: '{settings.QDRANT_API_KEY}'")
print(f"Boolean value: {bool(settings.QDRANT_API_KEY)}")
print(f"Length: {len(settings.QDRANT_API_KEY)}")
print(f"Strip value: '{settings.QDRANT_API_KEY.strip()}'")
print(f"Strip boolean: {bool(settings.QDRANT_API_KEY.strip())}")

# Check if it's truly empty
is_empty = settings.QDRANT_API_KEY == ""
print(f"Is truly empty string: {is_empty}")