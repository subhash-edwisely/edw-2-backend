from db import db
from datetime import datetime
import enum


class RoleEnum(enum.Enum):
    Student="student"
    Admin="admin"


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    hashed_password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum(RoleEnum), nullable=False, default=RoleEnum.Student)
    total_xp = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


    college_id = db.Column(db.Integer, db.ForeignKey("college.id"), nullable=False)
    college = db.relationship("College", back_populates="students")


    submissions = db.relationship("Submission", back_populates="user", cascade="all,delete-orphan", lazy="selectin")
    solved_problems = db.relationship("SolvedProblem", back_populates="user", cascade="all,delete-orphan", lazy="selectin")



    def __repr__(self):
        return f"<User {self.name} - {self.email} - {self.total_xp}>"