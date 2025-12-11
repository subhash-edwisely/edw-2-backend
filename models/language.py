from db import db
from datetime import datetime

class Language(db.Model):
    __tablename__ = "language"

    id = db.Column(db.Integer, primary_key=True)
    compiler_language_id = db.Column(db.Integer, nullable=False, unique=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # one-to-many-relationship
    snippets = db.relationship("Snippet", back_populates="language", cascade="all,delete-orphan", lazy="selectin")
    submission_answers = db.relationship("SubmissionAnswer", back_populates="language")


    def __repr__(self):
        return f"<Language {self.name}>"