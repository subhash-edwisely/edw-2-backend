from flask import request, jsonify
from services.aihints_service import AIHintService

def get_hints(problem_id):
    user_id = request.args.get("userId", type=int)

    hints = AIHintService.get_hints(problem_id, user_id)

    return jsonify({
        "success": True,
        "data": hints
    }), 200


def unlock_hint():
    data = request.get_json()
    user_id = data.get("userId")
    hint_id = data.get("hintId")

    if not user_id or not hint_id:
        return jsonify({
            "success": False,
            "message": "Missing userId or hintId"
        }), 400

    try:
        result = AIHintService.unlock_hint(user_id, hint_id)
        return jsonify({
            "success": True,
            "data": result
        }), 200

    except ValueError as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 400
