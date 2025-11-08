# app/app.py
from flask import Flask, request, jsonify
from datetime import datetime
from db import get_db
from utils import get_answer

app = Flask(__name__)

@app.route("/")
def home():
    """Health check endpoint."""
    return jsonify({"status": "AppstarAI Assistant is running"})

@app.route("/chat", methods=["POST"])
def chat():
    """
    Processes POST /chat requests.

    Expects JSON: {"user": "...", "message": "..."}
    Returns JSON: {"reply": "...", "matched": bool, "source": "exact"|"fuzzy"|"none"}
    """
    # read input
    data = request.get_json(force=True)
    message = (data.get("message") or "").strip()
    user = data.get("user", "guest")

    # get answer from utils.get_answer (returns (answer, matched, source))
    answer, matched, source = get_answer(message)

    # log to mongo
    db = get_db()
    try:
        db.conversations.insert_one({
            "user": user,
            "message": message,
            "answer": answer,
            "matched": matched,
            "source": source,
            "timestamp": datetime.utcnow()
        })
    except Exception as e:
        # do not fail the endpoint if DB logging fails; still return the reply
        app.logger.error("Failed to write conversation to DB: %s", e)

    # respond
    return jsonify({"reply": answer, "matched": matched, "source": source})

if __name__ == "__main__":
    # Development server (fine for local/dev). In prod, use gunicorn.
    app.run(host="0.0.0.0", port=8000)


