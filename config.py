import os, socket

class Config:
    VERSION = "1.0.0"
    PLATFORM = "molab"
    HOST = "0.0.0.0"
    PORT = int(os.environ.get("PORT", "8765"))
    TOKEN = os.environ.get("MOLAB_TOKEN", "magoco-secure-2026")
    
    # Adaptive intervals (Gaussian base)
    KA_MIN = 25 # mins
    KA_MAX = 80 # mins
    
    # Path settings
    LOG_DIR = "/tmp/molab-node/logs"
    os.makedirs(LOG_DIR, exist_ok=True)