from flask import Flask
import os
import socket

app = Flask(__name__)

@app.route("/")
def home():
    return f"Hello from container: {socket.gethostname()}\n"

@app.route("/health")
def health():
    return {"status": "ok"}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
