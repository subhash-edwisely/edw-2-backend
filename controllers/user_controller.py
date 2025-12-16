from flask import make_response
from services.user_service import fetch_all_users, fetch_user_by_id, register, login
from utils.response import success, error
from db import db
from models.user import User
from models.problem import Problem, DifficultyEnum
from models.solved_problem import SolvedProblem
from sqlalchemy import func
from datetime import datetime, timedelta


# ---------------- Users ----------------
def get_all_users():
    try:
        users = fetch_all_users()
        return success(data=users, status=200)
    except Exception as e:
        return error(str(e))


def get_user(user_id: int):
    try:
        user = fetch_user_by_id(user_id)
        if not user:
            return error("User not found", 404)
        return success(data=user, status=200)
    except Exception as e:
        return error(str(e))


def register_user(data):
    try:
        result = register(data)
        if not result:
            return error("User already exists", 400)

        response = make_response(success(
            message="User registered successfully",
            data=result["user"],
            status=201
        ))

        response.set_cookie(
            key="access_token",
            value=result["access_token"],
            max_age=7*24*60*60,
            path="/",
            secure=False,
            httponly=True,
            samesite="Lax"
        )
        return response
    except Exception as e:
        return error(str(e))


def login_user(data):
    try:
        result = login(data)
        if not result:
            return error("User does not exist", 404)
        if result == "Invalid password":
            return error("Invalid password", 401)

        response = make_response(success(
            message="User login successful",
            data=result["user"],
            status=200
        ))

        response.set_cookie(
            key="access_token",
            value=result["access_token"],
            max_age=7*24*60*60,
            path="/",
            secure=True,
            httponly=True,
            samesite="None"
        )

        return response
    except Exception as e:
        return error(str(e))


# ---------------- User Progress ----------------
def get_user_progress(user_id: int):
    user = User.query.get_or_404(user_id)

    # ---------------- Basic stats ----------------
    problems_solved_count = (
        db.session.query(func.count(SolvedProblem.id))
        .filter(SolvedProblem.user_id == user_id)
        .scalar()
    )
    total_problems = Problem.query.count()

    current_user = {
        "xp": user.total_xp or 0,
        "problemsSolved": problems_solved_count or 0,
        "totalProblems": total_problems or 0
    }

    # ---------------- Difficulty progress ----------------
    total_by_diff = dict(
        db.session.query(
            Problem.difficulty,
            func.count(Problem.id)
        ).group_by(Problem.difficulty).all()
    )

    solved_by_diff = dict(
        db.session.query(
            Problem.difficulty,
            func.count(SolvedProblem.id)
        )
        .join(SolvedProblem, SolvedProblem.problem_id == Problem.id)
        .filter(SolvedProblem.user_id == user_id)
        .group_by(Problem.difficulty)
        .all()
    )

    difficulty_progress = {}
    for diff in DifficultyEnum:
        key = diff.value.lower()
        difficulty_progress[key] = {
            "solved": solved_by_diff.get(diff, 0),
            "total": total_by_diff.get(diff, 0)
        }

    # ---------------- Weekly activity ----------------
    start_date = datetime.utcnow().date() - timedelta(days=6)
    daily_map = {start_date + timedelta(days=i): 0 for i in range(7)}

    weekly_rows = (
        db.session.query(
            func.date(SolvedProblem.solvedAt).label("day"),
            func.count(SolvedProblem.id)
        )
        .filter(
            SolvedProblem.user_id == user_id,
            SolvedProblem.solvedAt >= start_date
        )
        .group_by(func.date(SolvedProblem.solvedAt))
        .all()
    )

    for row in weekly_rows:
        daily_map[row.day] = row[1]

    weekly_activity = [
        {"day": (start_date + timedelta(days=i)).strftime("%a"), "problems": daily_map[start_date + timedelta(days=i)]}
        for i in range(7)
    ]

    return {
        "currentUser": current_user,
        "difficultyProgress": difficulty_progress,
        "weeklyActivity": weekly_activity
    }
