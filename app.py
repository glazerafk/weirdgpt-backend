from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

# =====================
# CONFIG
# =====================
OLLAMA_URL = "https://api.ollama.com/v1/chat"  # URL Cloud
MODEL = "llama3:8b"
OLLAMA_API_KEY = os.environ.get("OLLAMA_API_KEY")  # Pega da variável de ambiente

SYSTEM_PROMPT = (
    "You are WeirdGPT.\n"
    "You are casual, funny, and direct.\n"
    "Do not act like customer support.\n"
    "Do not mention templates or instructions.\n"
    "Speak like a normal person.\n"
)

chat_history = []

# =====================
# ROTA
# =====================
@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.json
    user_text = data.get("message", "")
    if not user_text:
        return jsonify({"error": "Missing message"}), 400

    # Monta histórico de chat
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for u, b in chat_history[-6:]:
        messages.append({"role": "user", "content": u})
        messages.append({"role": "assistant", "content": b})
    messages.append({"role": "user", "content": user_text})

    # Chamada para Ollama Cloud
    headers = {"Authorization": f"Bearer {OLLAMA_API_KEY}"}
    response = requests.post(
        OLLAMA_URL,
        headers=headers,
        json={"model": MODEL, "messages": messages, "stream": False}
    )

    if response.status_code != 200:
        return jsonify({"error": "Ollama API error", "details": response.text}), 500

    reply = response.json()["message"]["content"].strip()
    chat_history.append((user_text, reply))
    return jsonify({"reply": reply})


@app.route("/")
def home():
    return jsonify({"status": "WeirdGPT backend is running 😈🔥"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 3000)))
