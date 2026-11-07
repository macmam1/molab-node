
import os

class Config:
    VERSION = "1.0.0"
    PLATFORM = "molab"
    HOST = "0.0.0.0"
    
    # Anti-sleep intervals (Gaussian)
    KA_MIN = int(os.environ.get("KA_MIN", "25"))  # min
    KA_MAX = int(os.environ.get("KA_MAX", "80"))  # max
    
    LOG_FILE = "/tmp/molab-node/antisol.log"
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
