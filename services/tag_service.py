from models.tag import Tag
from models.problem_tag import ProblemTag
from models.problem import Problem
from sqlalchemy.orm import selectinload
from db import db


def fetch_all_tags():
    tags = Tag.query.all()
    return [
        {
            "id": t.id,
            "name": t.name,
            "category": t.category.value if t.category.value else "",
            "created_at": t.created_at,
            "problem_count": len(t.problems)

        } for t in tags
    ]



def fetch_tag_by_id(tag_id):
    tag = Tag.query.filter_by(id=tag_id).first()
    return {
            "id": tag.id,
            "name": tag.name,
            "category": tag.category.value if tag.category.value else None,
            "created_at": tag.created_at
        }


def fetch_problems_using_tag_id(tag_id):
    problems = (
        db.session.query(Problem)
        .join(ProblemTag, Problem.id == ProblemTag.problem_id)
        .filter(ProblemTag.tag_id == tag_id)
        .all()
    )

    return [
        {
            "id": p.id,
            "title": p.title,
            "description": p.description,
            "xp_reward": p.xp_reward,
            "created_at": p.created_at,
            "difficulty": p.difficulty.value if p.difficulty else None
        }
        for p in problems
    ]