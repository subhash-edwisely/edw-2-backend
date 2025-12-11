from flask import jsonify

from services.problem_service import (
    fetch_all_problems,
    fetch_problem_by_id,
    fetch_problem_editorial,
    fetch_problem_hints,
    fetch_problem_constraints,
    fetch_problem_snippets,
    fetch_problem_tags,
    fetch_problem_testcases,
    create_new_problem,
    fetch_daily_challenge
)


from utils.response import success, error


def get_all_problems():
    try:
        problems = fetch_all_problems()
        return success(data=problems)
    
    except Exception as e:
        return error(str(e))
    


def get_problem(problem_id: int):
    try:
        problem = fetch_problem_by_id(problem_id)
        if not problem:
            return error("Problem not found", 404)
        return success(data=problem)
    
    except Exception as e:
        return error(str(e))
    

def get_problem_editorial(problem_id: int):
    try:
        problem_editorial = fetch_problem_editorial(problem_id)
        if not problem_editorial:
            return error("Editorial not found", 404)
        return success(data=problem_editorial)
    
    except Exception as e:
        return error(str(e))
    

def get_problem_hints(problem_id: int):
    try:
        problem_hints = fetch_problem_hints(problem_id)
        if not problem_hints:
            return error("Hints not found", 404)
        return success(data=problem_hints)
    
    except Exception as e:
        return error(str(e))


def get_problem_constraints(problem_id: int):
    try:
        problem_constraints = fetch_problem_constraints(problem_id)
        if not problem_constraints:
            return error("Constraints not found", 404)
        return success(data=problem_constraints)    
    
    except Exception as e:
        return error(str(e))


def get_problem_snippets(problem_id: int):
    try:
        problem_snippets = fetch_problem_snippets(problem_id)
        if not problem_snippets:
            return error("Snippets not found", 404)
        return success(data=problem_snippets)    
    
    except Exception as e:
        return error(str(e))
        

def get_problem_tags(problem_id: int):
    try:
        problem_tags = fetch_problem_tags(problem_id)
        if not problem_tags:
            return error("Tags not found", 404)
        return success(data=problem_tags)    
    
    except Exception as e:
        return error(str(e))
    

def get_problem_testcases(problem_id: int):
    try:
        problem_testcases = fetch_problem_testcases(problem_id)
        if not problem_testcases:
            return error("Testcases not found", 404)
        return success(data=problem_testcases)    
    
    except Exception as e:
        return error(str(e))
    
def create_problem(data):
    try:
        problem = create_new_problem(data)
        print("Provlem : ", problem)

        if not problem:
            return error("Problem already exists")

        return success(data=problem, message="Problem created successfully")
    
    except Exception as e:
        return error(str(e))
    
def get_daily_challenge():
    try:
        daily_problem = fetch_daily_challenge()
        if not daily_problem:
            return error("No problems found", 404)
        return success(data=daily_problem)
    except Exception as e:
        return error(str(e))
