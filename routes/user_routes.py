from flask import Blueprint, request
from controllers.user_controller import (
    get_all_users,
    get_user,
    register_user,
    login_user,
    get_user_progress
)

user_bp = Blueprint("user_routes", __name__)

@user_bp.get("/")
def route_get_all_users():
    return get_all_users()

@user_bp.get("/<int:user_id>")
def route_get_user(user_id):
    return get_user(user_id)

@user_bp.post("/register")
def route_register_user():
    data = request.json
    return register_user(data)

@user_bp.post("/login")
def route_login_user():
    data = request.json
    return login_user(data)

# ⭐ NEW: GET USER PROGRESS
@user_bp.get("/<int:user_id>/progress")
def route_user_progress(user_id):
    return get_user_progress(user_id)
