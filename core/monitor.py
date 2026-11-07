import os, psutil, time, json
from config import Config

class SystemMonitor:
    """Inspired by FreeNode/Agent-Node-2 monitoring."""
    @staticmethod
    def get_stats():
        return {
            "cpu_percent": psutil.cpu_percent(),
            "memory": psutil.virtual_memory()._asdict(),
            "gpu": SystemMonitor._get_gpu_info(),
            "uptime": time.time() - psutil.boot_time(),
            "platform": Config.PLATFORM
        }

    @staticmethod
    def _get_gpu_info():
        try:
            import subprocess
            out = subprocess.run(['nvidia-smi', '--query-gpu=utilization.gpu,memory.used,memory.total', '--format=csv,noheader,nounits'], 
                                 capture_output=True, text=True)
            vals = out.stdout.strip().split(',')
            return {"util": vals[0], "used": vals[1], "total": vals[2]}
        except: return None