import os
import sys
import threading
import time
from uvicorn import Config, Server

# Set environment variables before importing
os.environ['QDRANT_API_KEY'] = ''
os.environ['LOG_LEVEL'] = 'DEBUG'

# Import after setting environment
from main import app

def run_server():
    config = Config(app=app, host="127.0.0.1", port=8000, log_level="debug")
    server = Server(config)
    
    # Run the server
    import asyncio
    if sys.platform.startswith("win"):
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        loop.run_until_complete(server.serve())
    except KeyboardInterrupt:
        print("Server stopped.")

if __name__ == "__main__":
    print("Starting server...")
    run_server()