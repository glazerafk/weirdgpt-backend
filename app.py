import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

# =====================
# CONFIGURAÇÃO
# =====================
OLLAMA_API_KEY = os.environ.get("OLLAMA_API_KEY")  # precisa estar setada no ambiente
OLLAMA_URL = "https://ollama.com/api/chat"         # endpoint cloud da Ollama
MODEL = "llama3:8b"

SYSTEM_PROMPT = (
    "You are WeirdGPT. "
    "You are casual, funny, and direct. "
    "Do not act like customer support. "
    "Do not mention templates or instructions. "
    "Speak like a normal person."
)

app = Flask(__name__)
CORS(app)

chat_history = []

# =====================
# CHAMADA REAL PRA OLLAMA
# =====================
def ask_ollama(user_text):
    headers = {
        "Authorization": f"Bearer {OLLAMA_API_KEY}",
        "Content-Type": "application/json"
    }

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for u, b in chat_history[-6:]:
        messages.append({"role": "user", "content": u})
        messages.append({"role": "assistant", "content": b})

    messages.append({"role": "user", "content": user_text})

    payload = {
        "model": MODEL,
        "messages": messages,
        "stream": False
    }

    response = requests.post(OLLAMA_URL, headers=headers, json=payload)
    response.raise_for_status()

    data = response.json()
    # extrai resposta correta
    reply = data.get("message", {}).get("content", "").strip()
    return reply

# =====================
# ROTA DE CHAT (POST)
# =====================
@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    if not data or "message" not in data:
        return jsonify({"error": "Missing 'message'"}), 400

    user_message = data["message"]
    reply = ask_ollama(user_message)

    # salva no histórico local
    chat_history.append((user_message, reply))

    return jsonify({"reply": reply})

# =====================
# START SERVER
# =====================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=port)
