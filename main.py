
import logging, sys, time
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("antisol.log"), logging.StreamHandler()]
)

if __name__ == "__main__":
    from core.keepalive import AntiSleep
    
    print(f"="="*50")
    print(f"MAGoCo Anti-Sleep Core v{Config.VERSION}")
    print(f"Molab | Adaptive Gaussian | GPU Heartbeat")
    print(f"="="*50")
    
    as = AntiSleep()
    as.start()
    
    # Keep main thread alive
    while True:
        time.sleep(60)
        # Probabilistic heartbeat to kernel itself (obscurity)
        logger.info("[MAGoCo] Active | Uptime %0.f mins", time.time() / 60)
