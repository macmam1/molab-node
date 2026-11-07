import logging, os
from config import Config
from core.keepalive import SmartKeepAlive
from access.api import start_api

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.FileHandler(f"{Config.LOG_DIR}/node.log"), logging.StreamHandler()]
)

if __name__ == "__main__":
    print(f"--- molab-node v{Config.VERSION} Starting ---")
    
    # 1. Start Smart Keep-Alive (Unified)
    ka = SmartKeepAlive()
    ka.start()
    
    # 2. Start Access API (from Agent-Node-2/FreeNode)
    print(f"API Server starting on port {Config.PORT}")
    start_api()