from ..db import db
from datetime import datetime

class Hint(db.Model):
    __tablename__ = "hint"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    problem_id = db.Column(db.Integer, db.ForeignKey("problem.id"), nullable=False)
    problem = db.relationship("Problem", back_populates="hints")


    def __repr__(self):
        return f"<Hint {self.id} for problem {self.problem_id}>"        