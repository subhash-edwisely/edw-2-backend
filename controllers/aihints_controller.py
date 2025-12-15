from flask import Blueprint, request, jsonify
from models.aihints import AIHint, UserAIHint
from models.user import User
from models.xp_transaction import XPTransaction, Feature, Source
from db import db
from datetime import datetime
import uuid

aihints_bp = Blueprint("aihints", __name__, url_prefix="/api/aihints")


def generate_uuid():
    return str(uuid.uuid4())


# GET /api/aihints/<problem_id>
@aihints_bp.route("/<int:problem_id>", methods=["GET"])
def get_hints(problem_id):
    user_id = request.args.get("userId")

    hints = (
        AIHint.query
        .filter_by(problem_id=problem_id)
        .order_by(AIHint.level)
        .all()
    )

    unlocked_hint_ids = set()
    if user_id:
        unlocked_hint_ids = {
            uh.hint_id
            for uh in UserAIHint.query.filter_by(user_id=int(user_id)).all()
        }

    result = []
    for hint in hints:
        is_unlocked = hint.id in unlocked_hint_ids

        result.append({
            "id": hint.id,
            "level": hint.level,
            "label": hint.label,
            "content": hint.content if is_unlocked or not hint.locked else None,
            "cost": hint.cost,
            "locked": hint.locked and not is_unlocked
        })

    return jsonify({
        "success": True,
        "data": result
    }), 200


# POST /api/aihints/unlock
@aihints_bp.route("/unlock", methods=["POST"])
def unlock_hint():
    data = request.json
    user_id = data.get("userId")
    hint_id = data.get("hintId")

    if not user_id or not hint_id:
        return jsonify({"error": "userId and hintId are required"}), 400

    user = User.query.get(int(user_id))
    hint = AIHint.query.get(hint_id)

    if not user or not hint:
        return jsonify({"error": "User or hint not found"}), 404

    already_unlocked = UserAIHint.query.filter_by(
        user_id=user.id,
        hint_id=hint.id
    ).first()

    if already_unlocked:
        return jsonify({"message": "Hint already unlocked"}), 200

    if user.totalXP < hint.cost:
        return jsonify({"error": "Not enough XP"}), 400

    # Deduct XP
    user.totalXP -= hint.cost

    user_hint = UserAIHint(
        id=generate_uuid(),
        user_id=user.id,
        hint_id=hint.id,
        xp_spent=hint.cost,
        unlocked_at=datetime.utcnow()
    )

    xp_txn = XPTransaction(
        id=generate_uuid(),
        user_id=user.id,
        amount=hint.cost,
        transaction_type="spent",
        source_id=Source.query.filter_by(name="ai_help").first().id,
        feature_id=Feature.query.filter_by(name="hint").first().id,
        reference_id=hint.id,
        description=f"Unlocked AI hint L{hint.level} for problem {hint.problem_id}"
    )

    db.session.add_all([user, user_hint, xp_txn])
    db.session.commit()

    return jsonify({
        "message": "Hint unlocked successfully",
        "hintId": hint.id,
        "remainingXP": user.totalXP
    }), 200
