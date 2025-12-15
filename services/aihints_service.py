from models.aihints import AIHint, UserAIHint
from models.user import User
from models.xp_transaction import XPTransaction, Feature, Source
from db import db
from datetime import datetime
import uuid


def generate_uuid():
    return str(uuid.uuid4())


class AIHintService:

    @staticmethod
    def get_hints(problem_id: int, user_id: int | None = None):
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
                for uh in UserAIHint.query.filter_by(user_id=user_id).all()
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

        return result

    @staticmethod
    def unlock_hint(user_id: int, hint_id: str):
        user = User.query.get(user_id)
        hint = AIHint.query.get(hint_id)

        if not user or not hint:
            raise ValueError("User or hint not found")

        already_unlocked = UserAIHint.query.filter_by(
            user_id=user.id,
            hint_id=hint.id
        ).first()

        if already_unlocked:
            return {
                "message": "Hint already unlocked",
                "hintId": hint.id
            }
        if user.total_xp < hint.cost:
            raise ValueError("Not enough XP")

        user.total_xp -= hint.cost

        

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
        return {
            "message": "Hint unlocked successfully",
            "hint": {
            "id": hint.id,
            "level": hint.level,
            "label": hint.label,
            "content": hint.content,
            "cost": hint.cost,
            "locked": False
             },
            "remainingXP": user.total_xp

        }
