# backend/routes/ai_routes.py
from flask import Blueprint, request, jsonify, current_app
import os
import requests

ai_bp = Blueprint("ai", __name__, url_prefix="/api/ai")

# In-memory chat history store (for demo; replace with DB if needed)
chat_history_store = {}

GEMINI_API_URL = os.environ.get("GEMINI_API_URL", "https://api.gemini.example.com/v1/chat")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

@ai_bp.route("/chat", methods=["POST"])
def chat():
    data = request.json
    problem_id = str(data.get("problemId"))
    message = data.get("message")
    code = data.get("code", "")

    if not problem_id or not message:
        return jsonify({"error": "Missing problemId or message"}), 400

    # Retrieve previous chat for context
    history = chat_history_store.get(problem_id, [])

    payload = {
        "messages": history + [{"role": "user", "content": message}],
        "context_code": code
    }

    headers = {
        "Authorization": f"Bearer {GEMINI_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(GEMINI_API_URL, json=payload, headers=headers)
        response.raise_for_status()
        ai_message = response.json().get("reply", "No response from AI.")

        # Save messages in chat history
        history.append({"role": "user", "content": message})
        history.append({"role": "ai", "content": ai_message})
        chat_history_store[problem_id] = history

        return jsonify({"message": ai_message, "history": history})

    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500


@ai_bp.route("/chat/history/<problem_id>", methods=["GET"])
def chat_history(problem_id):
    history = chat_history_store.get(str(problem_id), [])
    return jsonify({"history": history})
