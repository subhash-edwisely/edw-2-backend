from flask import Blueprint, request, jsonify
from services.aihints_service import AIHintService

aihints_bp = Blueprint("aihints", __name__, url_prefix="/api/aihints")

@aihints_bp.route("/<int:problem_id>", methods=["GET"])
def get_hints(problem_id):
    user_id = request.args.get("userId")  # optional but IMPORTANT

    try:
        hints = AIHintService.get_hints(problem_id, user_id)
        return jsonify({
            "success": True,
            "data": hints
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 400
  
@aihints_bp.route("/unlock", methods=["POST"])
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
        unlocked_hint = AIHintService.unlock_hint(user_id, hint_id)
        return jsonify({
            "success": True,
            "data": unlocked_hint
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500
      
        
