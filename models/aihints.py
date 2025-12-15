from datetime import datetime
from db import db  # SQLAlchemy instance
import uuid

# If you want to keep UUIDs as strings (works with MySQL)
def generate_uuid_str():
    return str(uuid.uuid4())

class AIHint(db.Model):
    __tablename__ = "aihints"

    id = db.Column(db.String(36), primary_key=True, default=generate_uuid_str)
    problem_id = db.Column(db.Integer, db.ForeignKey("problem.id", ondelete="CASCADE"), nullable=False)
    level = db.Column(db.Integer, nullable=False)
    label = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    cost = db.Column(db.Integer, default=0)
    locked = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    problem = db.relationship("Problem", backref=db.backref("aihints", lazy=True))


class UserAIHint(db.Model):
    __tablename__ = "user_aihints"

    id = db.Column(db.String(36), primary_key=True, default=generate_uuid_str)  # okay to keep UUID for this table
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    hint_id = db.Column(db.String(36), db.ForeignKey("aihints.id", ondelete="CASCADE"), nullable=False)
    xp_spent = db.Column(db.Integer, nullable=False)
    unlocked_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", backref=db.backref("user_aihints", lazy=True))
    hint = db.relationship("AIHint", backref=db.backref("user_aihints", lazy=True))

    __table_args__ = (
        db.UniqueConstraint('user_id', 'hint_id', name='unique_user_hint'),
    )
