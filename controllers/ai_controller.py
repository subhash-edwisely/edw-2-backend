from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity
from services.chat_service import (
    handle_user_message,
    get_chat_history_for_user
)

def send_ai_message():
    user_id = get_jwt_identity()
    data = request.get_json()

    problem_id = data.get("problemId")
    message = data.get("message")
    code = data.get("code", "")

    ai_response = handle_user_message(
        user_id=user_id,
        problem_id=problem_id,
        message=message,
        code=code
    )

    return jsonify({
        "sender": "ai",
        "text": ai_response
    }), 200


def get_chat_history(problem_id):
    user_id = get_jwt_identity()

    messages = get_chat_history_for_problem(
        user_id=user_id,
        problem_id=problem_id
    )

    return jsonify([
        {
            "sender": msg.role.value,
            "text": msg.content,
            "createdAt": msg.created_at.isoformat()
        }
        for msg in messages
    ]), 200
