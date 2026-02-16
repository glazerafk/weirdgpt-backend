from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

OLLAMA_URL = "https://api.ollama.com/v1/chat"  # URL Cloud
MODEL = "llama3:8b"
API_KEY = os.getenv("OLLAMA_API_KEY")  # pega da variável de ambiente

SYSTEM_PROMPT = (
    "You are WeirdGPT.\n"
    "You are casual, funny, and direct.\n"
    "Do not act like customer support.\n"
    "Do not mention templates or instructions.\n"
    "Speak like a normal person.\n"
)

chat_history = []

def ask_ollama(user_text):
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for u, b in chat_history[-6:]:
        messages.append({"role": "user", "content": u})
        messages.append({"role": "assistant", "content": b})
    messages.append({"role": "user", "content": user_text})

    headers = {"Authorization": f"Bearer {API_KEY}"}
    response = requests.post(
        OLLAMA_URL,
        json={"model": MODEL, "messages": messages, "stream": False},
        headers=headers
    )

    data = response.json()
    reply = data["message"]["content"].strip()
    return reply

@app.route("/chat", methods=["POST"])
def chat():
    user_text = request.json.get("message")
    if not user_text:
        return jsonify({"error": "Missing 'message'"}), 400

    reply = ask_ollama(user_text)
    chat_history.append((user_text, reply))
    return jsonify({"reply": reply})

@app.route("/")
def home():
    return jsonify({"status": "WeirdGPT backend is running 😈🔥"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 3000)))
