from db import db
from datetime import datetime
import enum

class HelpTypeEnum(enum.Enum):
    explain_question = "explain_question"
    hint = "hint"

class AIHelp(db.Model):
    __tablename__ = "ai_help"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    problem_id = db.Column(db.Integer, db.ForeignKey("problem.id"), nullable=False)
    help_type = db.Column(db.Enum(HelpTypeEnum), nullable=False)
    xp_cost = db.Column(db.Integer, nullable=False)
    prompt = db.Column(db.Text, nullable=False)
    response = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    user = db.relationship("User", backref=db.backref("ai_helps", lazy="dynamic"))
    problem = db.relationship("Problem", backref=db.backref("ai_helps", lazy="dynamic"))

    def __repr__(self):
        return f"<AIHelp {self.help_type} for User {self.user_id} - Problem {self.problem_id}>"
