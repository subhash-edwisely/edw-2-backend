from flask import Blueprint
from controllers.ai_controller import send_ai_message, get_chat_history
from flask_jwt_extended import jwt_required

ai_routes = Blueprint("ai_routes", __name__)

ai_routes.route("/chat", methods=["POST"])(jwt_required()(send_ai_message))

ai_routes.route(
    "/chat/history/<int:problem_id>",
    methods=["GET"]
)(jwt_required()(get_chat_history))
