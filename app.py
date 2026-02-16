from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

OLLAMA_URL = "https://api.ollama.com/v1/chat"  # bruh
MODEL = "llama3:8b"
SYSTEM_PROMPT = (
    "You are WeirdGPT.\n"
    "You are casual, funny, and direct.\n"
    "Do not act like customer support.\n"
    "Do not mention templates or instructions.\n"
    "Speak like a normal person.\n"
)

chat_history = []

@app.route("/")
def home():
    return jsonify({"status": "go to /chat here is just a test."})

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_message = data.get("message", "")
        history = data.get("history", [])

        # sla porra cu lixo
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        for u, b in history[-6:]:
            messages.append({"role": "user", "content": u})
            messages.append({"role": "assistant", "content": b})
        messages.append({"role": "user", "content": user_message})

        # ollama call
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "messages": messages,
                "stream": False
            }
        )
        response.raise_for_status()
        reply = response.json()["message"]["content"].strip()

        # atualiza historico
        chat_history.append((user_message, reply))

        return jsonify({"response": reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=port)
