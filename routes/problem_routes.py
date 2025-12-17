from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from controllers.problem_controller import (
    get_all_problems,
    get_problem,
    get_problem_editorial,
    get_problem_hints,
    get_problem_constraints,
    get_problem_snippets,
    get_problem_tags,
    get_problem_testcases,
    create_problem,
    get_daily_challenge
)




problem_bp = Blueprint("problem_routes", __name__)

# ------------------ ROUTES ------------------

@problem_bp.get("/")
@jwt_required()
def route_get_all_problems():
    user_id = str(get_jwt_identity())
    return get_all_problems(user_id)



@problem_bp.get("/<int:problem_id>")
@jwt_required()
def route_get_problem(problem_id):
    user_id = str(get_jwt_identity())
    print(user_id, request.cookies)
    return get_problem(problem_id, user_id)


# @problem_bp.get("/<int:problem_id>/editorial")
# def route_get_problem_editorial(problem_id):
#     return get_problem_editorial(problem_id)


# @problem_bp.get("/<int:problem_id>/hints")
# def route_get_problem_hints(problem_id):
#     return get_problem_hints(problem_id)


# @problem_bp.get("/<int:problem_id>/constraints")
# def route_get_problem_constraints(problem_id):
#     return get_problem_constraints(problem_id)


# @problem_bp.get("/<int:problem_id>/snippets")
# def route_get_problem_snippets(problem_id):
#     return get_problem_snippets(problem_id)


# @problem_bp.get("/<int:problem_id>/tags")
# def route_get_problem_tags(problem_id):
#     return get_problem_tags(problem_id)


# @problem_bp.get("/<int:problem_id>/testcases")
# def route_get_problem_testcases(problem_id):
#     return get_problem_testcases(problem_id)


@problem_bp.post("/create")
def route_create_problem():
    data = request.json
    return create_problem({})


@problem_bp.get("/daily")
@jwt_required()
def route_get_daily_challenge():
    user_id = str(get_jwt_identity())  # ✅ get current user id
    return get_daily_challenge(user_id)  # pass it to the controller



# delete problem

# update problem
