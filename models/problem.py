from db import db
from datetime import datetime
import enum


class DifficultyEnum(enum.Enum):
    Easy = "Easy"
    Medium = "Medium"
    Hard = "Hard"


class Problem(db.Model):
    __tablename__ = "problem"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=False)
    difficulty = db.Column(db.Enum(DifficultyEnum), nullable=False, default=DifficultyEnum.Easy)
    xp_reward = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    accepted_submissions = db.Column(db.Integer, default=0, nullable=False)
    total_submissions = db.Column(db.Integer, default=0, nullable=False)
    acceptance_rate = db.Column(db.Float, default=55.0, nullable=False)


    # one-to-one    
    editorial = db.relationship("Editorial", back_populates="problem", cascade="all,delete-orphan", lazy="joined", uselist=False)

    # one-to-many
    hints = db.relationship("Hint", back_populates="problem", cascade="all,delete-orphan", lazy="selectin")
    constraints = db.relationship("Constraint", back_populates="problem", cascade="all,delete-orphan", lazy="selectin")
    snippets = db.relationship("Snippet", back_populates="problem", cascade="all,delete-orphan", lazy="selectin")
    testcases = db.relationship("Testcase", back_populates="problem", cascade="all,delete-orphan", lazy="selectin")
    submissions = db.relationship("Submission", back_populates="problem", cascade="all,delete-orphan", lazy="selectin")
    testcase_results = db.relationship("TestcaseResult", back_populates="problem", cascade="all,delete-orphan", lazy="selectin")
    solved_users = db.relationship("SolvedProblem", back_populates="problem", cascade="all,delete-orphan", lazy="selectin")


    # many-to-many (b/w problem and tag via problem_tag)
    tags =  db.relationship("ProblemTag", back_populates="problem", cascade="all,delete-orphan", lazy="selectin")



    def __repr__(self):
        return f"<Problem {self.title}>"