from flask import Blueprint


tag_bp = Blueprint("tag_routes", __name__)

# ------------------ ROUTES ------------------

@tag_bp.get("/")
def route_get_all_tags():
    return 