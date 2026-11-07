# molab-node
**MAGoCo Unified Always-On Core for Molab & Cloud Notebooks**

Combines the best features from:
- `titan-node` — adaptive keepalive, platform detection, SSH/Tunnel
- `freenode` — deception layer, monitoring dashboard, obfuscation
- `agent-node-2` — WebSocket terminal, sshx, token bootstrap

## Features
- **Smart Keep-Alive**: Gaussian interval (25-80 min) + GPU matmul activity
- **Health API**: `/health` + `/stats` (token protected)
- **System Monitor**: CPU, RAM, GPU metrics
- **Auto-Detects**: Molab, Suga, Belmo, Docker

## Quick Start
```bash
pip install -r requirements.txt
python3 main.py
```

## Environment Variables
| Var | Default | Description |
|-----|---------|-------------|
| PORT | 8765 | API port |
| MOLAB_TOKEN | magoco-secure-2026 | API auth token |
| KA_MIN | 25 | Min keepalive interval (min) |
| KA_MAX | 80 | Max keepalive interval (min) |
