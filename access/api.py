from flask import Flask, jsonify, request
from core.monitor import SystemMonitor
from config import Config

app = Flask(__name__)

@app.route('/health')
def health():
    return jsonify({"status": "ok", "platform": Config.PLATFORM})

@app.route('/stats')
def stats():
    # Only allow with token (Agent-Node-2 security)
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    if token != Config.TOKEN:
        return jsonify({"error": "unauthorized"}), 401
    return jsonify(SystemMonitor.get_stats())

def start_api():
    app.run(host=Config.HOST, port=Config.PORT, threaded=True)