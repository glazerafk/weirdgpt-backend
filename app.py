import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

# =====================
# CONFIGURAÇÕES
# =====================
OLLAMA_URL = "https://api.ollama.com/v1/chat"
MODEL = "llama3:8b"
OLLAMA_API_KEY = os.environ.get("OLLAMA_API_KEY")  # coloque sua API Key aqui

SYSTEM_PROMPT = (
    "You are WeirdGPT.\n"
    "You are casual, funny, and direct.\n"
    "Do not act like customer support.\n"
    "Do not mention templates or instructions.\n"
    "Speak like a normal person.\n"
)

# =====================
# INICIA APP
# =====================
app = Flask(__name__)
CORS(app)

chat_history = []

# =====================
# CHAMADA AO MODELO
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

    response = requests.post(
        OLLAMA_URL,
        headers=headers,
        json={
            "model": MODEL,
            "messages": messages,
            "stream": False
        }
    )

    data = response.json()
    return data.get("message", {}).get("content", "").strip()

# =====================
# ROTA PRINCIPAL
# =====================
@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "")
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    reply = ask_ollama(user_message)
    chat_history.append((user_message, reply))
    return jsonify({"reply": reply})

# =====================
# RODA SERVER
# =====================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=port)
