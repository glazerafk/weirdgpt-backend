import os
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return jsonify({"status": "WeirdGPT backend is running 😈🔥"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))  # Pega a porta do Render, ou usa 3000 localmente
    app.run(host="0.0.0.0", port=port)
