from db import db
from datetime import datetime
import enum


class CategoryEnum(enum.Enum):
    Topic = "Topic"
    Company = "Company"


class Tag(db.Model):
    __tablename__ = "tag"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    category = db.Column(db.Enum(CategoryEnum), nullable=False, default=CategoryEnum.Topic)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


    # many-to-many (b/w problem and tag via problem_tag)
    problems = db.relationship("ProblemTag", back_populates="tag", lazy="selectin", cascade="all,delete-orphan")


    def __repr__(self):
        return f"<Tag {self.name}>"

