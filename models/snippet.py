from ..db import db
from datetime import datetime

class Snippet(db.Model):
    __tablename__ = "snippet"

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


    problem_id = db.Column(db.Integer, db.ForeignKey("problem.id"), nullable=False)
    language_id = db.Column(db.Integer, db.ForeignKey("language.id"), nullable=False)

    # relationships
    problem = db.relationship("Problem", back_populates="snippets")
    language = db.relationship("Language", back_populates="snippets")


    def __repr__(self):
        return f"<Snippet {self.id} for problem {self.problem_id}>"