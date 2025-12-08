from models.problem import Problem
from models.editorial import Editorial
from models.hint import Hint
from models.constraint import Constraint
from models.snippet import Snippet
from models.problem_tag import ProblemTag
from models.tag import Tag
from models.language import Language
from models.testcase import Testcase
from db import db




def fetch_all_problems():
    problems = Problem.query.all()
    return [
        {
            "id": p.id,
            "title": p.title,
            "description": p.description,
            "difficulty": p.difficulty,
            "xp_reward": p.xp_reward,
            "created_at": p.created_at
        } for p in problems
    ]




def fetch_problem_by_id(problem_id: int):
    problem = Problem.query.get(problem_id)
    if not problem:
        return None
    
    return {
            "id": problem.id,
            "title": problem.title,
            "description": problem.description,
            "difficulty": problem.difficulty,
            "xp_reward": problem.xp_reward,
            "created_at": problem.created_at
        }





def fetch_problem_editorial(problem_id: int):
    editorial = Editorial.query.filter_by(problem_id=problem_id).first()
    if not editorial:
        return None
    
    return {
        "id": editorial.id,
        "problem_id": editorial.problem_id,
        "content": editorial.content_markdown,
        "videoUrl": editorial.videoUrl,
        "created_at": editorial.created_at
    }






def fetch_problem_hints(problem_id: int):
    hints = Hint.query.filter_by(problem_id=problem_id).order_by(Hint.order).all()

    return [
        {
            "id": h.id,
            "problem_id": h.problem_id,
            "content": h.content,
            "order": h.order,
            "created_at": h.created_at
        }

        for h in hints
    ]





def fetch_problem_constraints(problem_id: int):
    constraints = Constraint.query.filter_by(problem_id=problem_id).order_by(Constraint.order).all()


    return [
        {
            "id": c.id,
            "problem_id": c.problem_id,
            "content": c.description,
            "order": c.order,
            "created_at": c.created_at
        }

        for c in constraints
    ]


   

def fetch_problem_snippets(problem_id: int):
    snippets = Snippet.query.filter_by(problem_id=problem_id).all()


    return [
        {
            "id": s.id,
            "problem_id": s.problem_id,
            "code": s.code,
            "language_name": s.language.name if s.language else None,
            "created_at": s.created_at
        }

        for s in snippets
    ]




def fetch_problem_tags(problem_id: int):
    tags = ProblemTag.query.filter_by(problem_id=problem_id).all()

    return [
        {
            "id": t.tag_id,
            "name": t.tag.name if t.tag else None,
            "category": t.tag.category if t.tag else None,
        }

        for t in tags
    ]


def fetch_problem_testcases(problem_id: int):
    testcases = Testcase.query.filter_by(problem_id=problem_id).order_by(Testcase.order).all()

    return [
        {
            "id": tc.id,
            "input": tc.input_data,
            "expected_output": tc.expected_output,
            "explanation": tc.explanation,
            "isHidden": tc.isHidden,
            "order": tc.order,
            "created_at": tc.created_at
        }
        
        for tc in testcases
    ]

def create_new_problem(data: dict):
    
    data = {
        "title": "Two Sum",
        "description": "Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.\n\nYou may assume that each input would have exactly one solution, and you may not use the same element twice.\n\nYou can return the answer in any order.",
        "xpReward": 10,
        "difficulty": "Easy",
        "hints": [
            {
                "content": "Try using a hash map to store the numbers you've seen so far.",
                "order": 1
            },
            {
                "content": "For each number, check if target - current number exists in your hash map.",
                "order": 2
            },
            {
                "content": "The time complexity can be reduced to O(n) with this approach.",
                "order": 3
            }
        ],

        "constraints": [
            {
                "description": "2 <= nums.length <= 10^4",
                "order": 1
            },
            {
                "description": "-10^9 <= nums[i] <= 10^9",
                "order": 2
            },
            {
                "description": "-10^9 <= target <= 10^9",
                "order": 3
            },
            {
                "description": "Only one valid answer exists",
                "order": 4
            }
        ]

    }