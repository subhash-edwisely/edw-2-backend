# routes/ai.py
from flask import Blueprint, request, jsonify
from services.openai_client import client, MODEL

ai_bp = Blueprint("ai", __name__, url_prefix="/api/ai")

@ai_bp.route("/chat", methods=["POST"])
def ai_chat():
    data = request.json
    problem_id = data.get("problemId")
    user_message = data.get("message", "")
    user_code = data.get("code", "")

    system_prompt = f"""
You are an AI coding assistant.
Help the user solve programming problems without directly giving final answers.
Guide step-by-step.

User code:
{user_code}
"""

    try:
        response = client.responses.create(
            model=MODEL,
            input=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            max_output_tokens=400,
            temperature=0.4
        )

        ai_text = response.output_text

        return jsonify({
            "success": True,
            "data": {
                "text": ai_text
            }
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500
