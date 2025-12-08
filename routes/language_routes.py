from flask import Blueprint

language_bp = Blueprint("language_routes", __name__)

# ------------------ ROUTES ------------------

@language_bp.get("/")
def route_get_all_languages():
    return 