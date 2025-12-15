from flask import Blueprint, request, jsonify
import os
import requests

ai_bp = Blueprint("ai", __name__, url_prefix="/api/ai")

chat_history_store = {}

GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent"
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")


@ai_bp.route("/chat", methods=["POST"])
def chat():
    data = request.json
    problem_id = str(data.get("problemId"))
    message = data.get("message")
    code = data.get("code", "")

    if not problem_id or not message:
        return jsonify({"error": "Missing problemId or message"}), 400

    history = chat_history_store.get(problem_id, [])

    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": f"""
You are an expert coding assistant.

User message:
{message}

User code:
{code}
"""
                    }
                ]
            }
        ]
    }

    try:
        response = requests.post(
            f"{GEMINI_API_URL}?key={GEMINI_API_KEY}",
            headers={"Content-Type": "application/json"},
            json=payload,
            timeout=30,
        )
        response.raise_for_status()

        ai_message = (
            response.json()["candidates"][0]
            ["content"]["parts"][0]
            ["text"]
        )

        history.append({"role": "user", "content": message})
        history.append({"role": "assistant", "content": ai_message})
        chat_history_store[problem_id] = history

        return jsonify({"message": ai_message, "history": history})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@ai_bp.route("/chat/history/<problem_id>", methods=["GET"])
def chat_history(problem_id):
    history = chat_history_store.get(str(problem_id), [])
    return jsonify({"history": history})
