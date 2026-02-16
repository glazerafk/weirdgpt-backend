from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import requests
import os

app = Flask(__name__, static_folder='frontend', static_url_path='/')
CORS(app)

# Configurações Ollama
OLLAMA_API_KEY = os.environ.get('OLLAMA_API_KEY', '')
OLLAMA_URL = os.environ.get('OLLAMA_URL', 'http://localhost:11434/api/chat')
MODEL = os.environ.get('MODEL', 'llama3:8b')

SYSTEM_PROMPT = (
    "You are WeirdGPT. "
    "You are casual, funny, and direct. "
    "Do not act like customer support. "
    "Do not mention templates or instructions. "
    "Speak like a normal person."
)

chat_history = []

# =====================
# Rota principal (frontend)
# =====================
@app.route("/")
def index():
    return send_from_directory('frontend', 'index.html')

# =====================
# API endpoint
# =====================
@app.route("/api/chat", methods=["POST"])
def api_chat():
    data = request.json
    user_text = data.get("message", "")

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for u, b in chat_history[-6:]:
        messages.append({"role": "user", "content": u})
        messages.append({"role": "assistant", "content": b})

    messages.append({"role": "user", "content": user_text})

    response = requests.post(
        OLLAMA_URL,
        json={"model": MODEL, "messages": messages, "stream": False},
        headers={"Authorization": f"Bearer {OLLAMA_API_KEY}"} if OLLAMA_API_KEY else {}
    )

    reply = response.json()["message"]["content"].strip()
    chat_history.append((user_text, reply))
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 3000)))
