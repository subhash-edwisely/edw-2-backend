from db import db
from datetime import datetime
import uuid

def uuid_str():
    return str(uuid.uuid4())

class ChatSession(db.Model):
    __tablename__ = "chat_sessions"

    id = db.Column(db.String(36), primary_key=True, default=uuid_str)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    problem_id = db.Column(db.Integer, db.ForeignKey("problem.id", ondelete="CASCADE"), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_message_at = db.Column(db.DateTime, default=datetime.utcnow)

    # relationships
    user = db.relationship("User", backref=db.backref("chat_sessions", lazy="selectin"))
    problem = db.relationship("Problem", backref=db.backref("chat_sessions", lazy="selectin"))
    messages = db.relationship(
        "ChatMessage",
        back_populates="session",
        cascade="all, delete-orphan",
        order_by="ChatMessage.created_at",
    )

    __table_args__ = (
        db.UniqueConstraint("user_id", "problem_id", name="unique_user_problem_chat"),
    )
