from flask import Flask, request, jsonify
import json
import os
import socket

app = Flask(__name__)
DATA_FILE = "memory.json"

# Load memory kalau ada
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        memory = json.load(f)
else:
    memory = {}

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    msg = data.get("message", "").lower()

    # Format ajarin: "ajarin kata = arti"
    if msg.startswith("ajarin "):
        try:
            _, rest = msg.split(" ", 1)
            key, val = rest.split("=", 1)
            key = key.strip()
            val = val.strip()
            memory[key] = val
            with open(DATA_FILE, "w") as f:
                json.dump(memory, f)
            return jsonify({"reply": f"Oke, aku ingat '{key}' = '{val}'"})
        except:
            return jsonify({"reply": "Format salah. Gunakan: ajarin kata = arti"})

    if msg in memory:
        return jsonify({"reply": memory[msg]})

    return jsonify({"reply": "Aku belum tahu itu. Ajarin aku pakai: ajarin kata = arti"})


@app.route("/get_ip")
def get_ip():
    # Cari IP lokal server (non-loopback)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except:
        ip = "127.0.0.1"
    finally:
        s.close()
    return jsonify({"ip": ip})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
