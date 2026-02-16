from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "WeirdGPT backend is running 😈🔥"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    message = data.get("message", "")

    reply = f"WeirdGPT says: {message}"

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
