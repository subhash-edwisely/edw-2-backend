from ..db import db
from datetime import datetime

class Constraint(db.Model):
    __tablename__ = "constraint"

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False)
    order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    problem_id = db.Column(db.Integer, db.ForeignKey("problem.id"), nullable=False)
    problem = db.relationship("Problem", back_populates="constraints")


    def __repr__(self):
        return f"<Constraint {self.id} for problem {self.problem_id}>"   