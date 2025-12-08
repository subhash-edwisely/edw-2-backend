from ..db import db
from datetime import datetime


class Editorial(db.Model):
    __tablename__ = "editorial"
    id = db.Column(db.Integer, primary_key=True)
    content_markdown = db.Column(db.Text, nullable=True)
    content_html = db.Column(db.Text, nullable=True)
    videoUrl = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    problem_id = db.Column(db.Integer, db.ForeignKey("problem.id"), nullable=False, unique=True)
    problem = db.relationship("Problem", back_populates="editorial")

    def __repr__(self):
        return f"<Editorial for problem_id={self.problem_id}>"