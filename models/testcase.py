from db import db
from datetime import datetime

class Testcase(db.Model):
    __tablename__ = "testcase"

    id = db.Column(db.Integer, primary_key=True)
    input_data = db.Column(db.Text, nullable=False)
    expected_output = db.Column(db.Text, nullable=False)
    explanation = db.Column(db.Text, nullable=True)
    isHidden = db.Column(db.Boolean, default=False)
    order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)    



    problem_id = db.Column(db.Integer, db.ForeignKey("problem.id"), nullable=False)
    problem = db.relationship("Problem", back_populates="testcases")

    testcase_results = db.relationship("TestcaseResult", back_populates="testcase", cascade="all,delete-orphan", lazy="selectin")



    def __repr__(self):
        return f"<Testcase {self.id} for problem {self.problem_id}>"
