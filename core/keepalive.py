
import threading, time, random, logging, os
import torch
from config import Config

logger = logging.getLogger("molab-node")

class AntiSleep:
    """Unified anti-sleep/sleep prevention for Molab / Suga / Belmo / generic."""
    def __init__(self):
        self.pings = 0  # Track keepalive attempts
        self.stop_event = threading.Event()
        self.state_file = "/tmp/molab_node_state.json"
    
    def _gpu_keepalive(self):
        try:
            if torch.cuda.is_available():
                # Heartbeat of GPU compute: lightweight matmul
                _ = torch.randn(12,12,device='cuda') @ torch.randn(12,12,device='cuda')
                torch.cuda.synchronize()
                return True
        except: pass
        return False
    
    def _save_state(self):
        import json
        with open(self.state_file, "w") as f:
            json.dump({"pings": self.pings, "last": time.ctime()}, f)
    
    def anti_sleep_loop(self):
        """Main loop: adaptive interval + GPU heartbeat."""
        logger.info(f"[MAGoCo] Anti-Sleep started on platform={Config.PLATFORM}")
        
        while not self.stop_event.is_set():
            self.pings += 1
            gpu_ok = self._gpu_keepalive()
            self._save_state()
            
            logger.info(f"[MAGoCo] Keepalive #{self.pings} | GPU: {gpu_ok} | Interval: {self.last_interval}s")
            
            # Titan-style Gaussian interval (target 45m ± noise)
            target = (Config.KA_MIN + Config.KA_MAX) / 2 * 60
            std = (Config.KA_MAX - Config.KA_MIN) / 4 * 60
            delay = max(Config.KA_MIN*60, min(Config.KA_MAX*60, random.gauss(target, std)))
            self.last_interval = int(delay / 60)
            
            if self.stop_event.wait(delay): break
        
        logger.info("[MAGoCo] Anti-Sleep loop stopped")
    
    def start(self):
        t = threading.Thread(target=self.anti_sleep_loop, daemon=True, name="molab-anti-sleep")
        t.start()
        logger.info("Anti-Sleep thread | Daemon | Running")
        return t
