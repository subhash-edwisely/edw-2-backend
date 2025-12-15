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
