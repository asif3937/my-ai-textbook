from config.settings import settings

print(f"QDRANT_API_KEY: '{settings.QDRANT_API_KEY}'")
print(f"Boolean value: {bool(settings.QDRANT_API_KEY)}")
print(f"Length: {len(settings.QDRANT_API_KEY)}")
print(f"Strip value: '{settings.QDRANT_API_KEY.strip()}'")
print(f"Strip boolean: {bool(settings.QDRANT_API_KEY.strip())}")