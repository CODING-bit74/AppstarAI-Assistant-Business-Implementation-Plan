from flask import Flask, request, jsonify
from datetime import datetime
from db import get_db
from utils import get_answer

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"status": "AppstarAI Assistant is running"})

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(force=True)
    message = data.get("message", "").strip()
    user = data.get("user", "guest")

    answer = get_answer(message)
    matched = answer is not None

    if not matched:
        answer = "I'm not sure about that yet 🤔"

    db = get_db()
    db.conversations.insert_one({
        "user": user,
        "message": message,
        "answer": answer,
        "matched": matched,
        "timestamp": datetime.utcnow()
    })

    return jsonify({"reply": answer, "matched": matched})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

