from db import db
from datetime import datetime

class ProblemTag(db.Model):
    __tablename__ = "problem_tag"
    
    id = db.Column(db.Integer, primary_key=True)
    problem_id = db.Column(db.Integer, db.ForeignKey("problem.id"), nullable=False)
    tag_id = db.Column(db.Integer, db.ForeignKey("tag.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


    problem = db.relationship("Problem", back_populates="tags")
    tag = db.relationship("Tag", back_populates="problems", lazy="joined")


    __table_args__ = (
        db.UniqueConstraint('problem_id', 'tag_id', name='unique_problem_tag'),
    )


    def __repr__(self):
        return f"<ProblemTag problem={self.problem_id} tag={self.tag_id}>"
