from db import db
from datetime import datetime



class Submission(db.Model):
    __tablename__ = "submission"

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    total_exec_time = db.Column(db.Float)
    total_exec_memory = db.Column(db.Float)
    language_name = db.Column(db.String(255))



    submission_answer = db.relationship("SubmissionAnswer", back_populates="submission", cascade="all,delete-orphan", lazy="selectin")


    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user = db.relationship("User", back_populates="submissions")

    problem_id = db.Column(db.Integer, db.ForeignKey("problem.id"), nullable=False)
    problem = db.relationship("Problem", back_populates="submissions")


    testcase_results = db.relationship("TestcaseResult", back_populates="submission", cascade="all,delete-orphan", lazy="selectin")



    def __repr__(self):
        return f"<Submission {self.id} - problem {self.user_id} - user {self.problem_id}>"