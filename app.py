# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

# =====================
# CONFIGURAÇÃO
# =====================
OLLAMA_API_KEY = os.environ.get("OLLAMA_API_KEY")  # Coloque sua chave aqui ou em variável de ambiente
MODEL = "llama3:8b"
OLLAMA_URL = "https://api.ollama.com/v1/chat"

SYSTEM_PROMPT = (
    "You are WeirdGPT.\n"
    "You are casual, funny, and direct.\n"
    "Do not act like customer support.\n"
    "Do not mention templates or instructions.\n"
    "Speak like a normal person.\n"
)

# =====================
# ROTA DE TESTE
# =====================
@app.route("/")
def home():
    return jsonify({"status": "WeirdGPT backend is running 😈🔥"})

# =====================
# ROTA DE CHAT
# =====================
@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    if not data or "message" not in data:
        return jsonify({"error": "Missing 'message' field"}), 400

    user_text = data["message"]
    chat_history = data.get("history", [])

    # Monta as mensagens para o Ollama
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for u, b in chat_history[-6:]:  # mantém só últimas 6 mensagens
        messages.append({"role": "user", "content": u})
        messages.append({"role": "assistant", "content": b})
    messages.append({"role": "user", "content": user_text})

    headers = {
        "Authorization": f"Bearer {OLLAMA_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(
            OLLAMA_URL,
            json={"model": MODEL, "messages": messages, "stream": False},
            headers=headers,
            timeout=30
        )
        response.raise_for_status()
        data = response.json()
        reply = data["message"]["content"].strip()
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# =====================
# EXECUÇÃO
# =====================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=port)
