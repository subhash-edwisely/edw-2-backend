from ..db import db
from datetime import datetime
import enum


class DifficultyEnum(enum.Enum):
    Easy = "Easy"
    Medium = "Medium"
    Hard = "Hard"


class Problem(db.Model):
    __tablename_ = "problem"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=False)
    difficulty = db.Column(db.Enum(DifficultyEnum), nullable=False, default=DifficultyEnum.Easy)
    xp_reward = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


    # one-to-one
    editorial = db.relationship("Editorial", back_populates="problem", cascade="all,delete-orphan", lazy="dynamic")

    # one-to-many
    hints = db.relationship("Hint", back_populates="problem", cascade="all,delete-orphan", lazy="dynamic")
    constraints = db.relationship("Constraint", back_populates="problem", cascade="all,delete-orphan", lazy="dynamic")
    snippets = db.relationship("Snippet", back_populates="problem", cascade="all,delete-orphan", lazy="dynamic")
    testcases = db.relationship("Testcase", bacl_populates="problem", cascade="all,delete-orphan", lazy="dynamic")


    # many-to-many (b/w problem and tag via problem_tag)
    tags =  db.relationship("ProblemTag", back_populates="problem", cascade="all,delete-orphan", lazy="dynamic")



    def __repr__(self):
        return f"<Problem {self.title}>"