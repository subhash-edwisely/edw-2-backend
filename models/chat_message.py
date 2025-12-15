from db import db
from datetime import datetime
import enum
import uuid

def uuid_str():
    return str(uuid.uuid4())

class MessageRole(enum.Enum):
    user = "user"
    ai = "ai"
    system = "system"

class ChatMessage(db.Model):
    __tablename__ = "chat_messages"

    id = db.Column(db.String(36), primary_key=True, default=uuid_str)

    session_id = db.Column(
        db.String(36),
        db.ForeignKey("chat_sessions.id", ondelete="CASCADE"),
        nullable=False
    )

    role = db.Column(db.Enum(MessageRole), nullable=False)
    content = db.Column(db.Text, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    session = db.relationship("ChatSession", back_populates="messages")
