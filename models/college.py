from db import db
from datetime import datetime


class College(db.Model):
    __tablename__ = "college"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


    students = db.relationship("User", back_populates="college", cascade="all,delete-orphan", lazy="selectin")


    def __repr__(self):
        return f"<College {self.name}>"