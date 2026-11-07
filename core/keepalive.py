import threading, time, random, logging, os
import torch
from config import Config

logger = logging.getLogger("molab-node")

class SmartKeepAlive:
    """Combines Titan-node adaptive loop with kernel-level GPU activity."""
    def __init__(self):
        self.pings = 0
        self.stop_event = threading.Event()
        self.state_file = "/tmp/molab_node_state.json"

    def _gpu_activity(self):
        try:
            if torch.cuda.is_available():
                # Light matmul to keep CUDA context and GPU session active
                _ = torch.randn(10, 10, device='cuda') @ torch.randn(10, 10, device='cuda')
                torch.cuda.synchronize()
                return True
        except: pass
        return False

    def _save_state(self):
        import json
        with open(self.state_file, "w") as f:
            json.dump({"pings": self.pings, "last": time.ctime()}, f)

    def loop(self):
        logger.info("Keep-alive loop started.")
        while not self.stop_event.is_set():
            self.pings += 1
            gpu_ok = self._gpu_activity()
            self._save_state()
            
            logger.info(f"Ping #{self.pings} | GPU: {gpu_ok}")
            
            # Titan-node style: Gaussian interval
            target = (Config.KA_MIN + Config.KA_MAX) / 2 * 60
            std = (Config.KA_MAX - Config.KA_MIN) / 4 * 60
            delay = max(Config.KA_MIN*60, min(Config.KA_MAX*60, random.gauss(target, std)))
            
            if self.stop_event.wait(delay): break

    def start(self):
        t = threading.Thread(target=self.loop, daemon=True, name="molab-ka")
        t.start()
        return t