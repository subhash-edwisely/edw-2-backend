from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from controllers.submission_controller import (
    get_submissions_of_user_for_problem,
    get_submissions_of_user,
    create_submission
)



submission_bp = Blueprint("submission_routes", __name__)


@submission_bp.get("/<int:user_id>")
def route_get_submissions_of_user(user_id):
    return get_submissions_of_user(user_id)



@submission_bp.get("/<int:user_id>/<int:problem_id>")
def route_get_submissions_of_user_for_problem(user_id, problem_id):
    return get_submissions_of_user_for_problem(user_id, problem_id)


@submission_bp.post("/create")
@jwt_required()
def route_create_submission():
    data = request.json
    user_id = get_jwt_identity()

    data["user_id"] = user_id
    return create_submission(data)

