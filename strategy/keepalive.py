import threading, time, random, torch

def adaptive_ping():
    while True:
        # 1. Human-like jitter
        time.sleep(random.uniform(25*60, 80*60))
        # 2. Activity: torch matmul
        try:
            x = torch.randn(8,8,device='cuda') @ torch.randn(8,8,device='cuda')
            torch.cuda.synchronize()
        except: pass
        print(f"[MAGoCo-Molab] Keepalive activity at {time.ctime()}")

def run():
    threading.Thread(target=adaptive_ping, daemon=True).start()