from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.chat_service import handle_user_message, get_chat_history_for_user

ai_routes = Blueprint("ai_routes", __name__, url_prefix="/api/ai")

# POST /chat - send a message to AI
@ai_routes.route("/chat", methods=["POST"])
@jwt_required()
def send_message():
    user_id = get_jwt_identity()
    data = request.get_json()
    problem_id = data.get("problemId")
    message = data.get("message")
    code = data.get("code", "")

    if not problem_id or not message:
        return jsonify({
            "success": False,
            "message": "Missing problemId or message"
        }), 400

    try:
        ai_response = handle_user_message(
            user_id=user_id,
            problem_id=problem_id,
            message=message,
            code=code
        )
        return jsonify({
            "success": True,
            "response": ai_response
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

# GET /chat/history/<problem_id> - fetch chat history
@ai_routes.route("/chat/history/<int:problem_id>", methods=["GET"])
@jwt_required()
def fetch_chat_history(problem_id):
    user_id = get_jwt_identity()

    try:
        history = get_chat_history_for_user(user_id, problem_id)
        return jsonify({
            "success": True,
            "data": history
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500
