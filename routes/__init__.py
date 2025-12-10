from flask import Blueprint

from .user_routes import user_bp
from .problem_routes import problem_bp
from .language_routes import language_bp
from .tag_routes import tag_bp
from .root_routes import root_bp
from .submission_routes import submission_bp


def register_routes(app):
    app.register_blueprint(root_bp)
    app.register_blueprint(user_bp, url_prefix="/api/v1/users")
    app.register_blueprint(problem_bp, url_prefix="/api/v1/problems")
    app.register_blueprint(language_bp, url_prefix="/api/v1/languages")
    app.register_blueprint(tag_bp, url_prefix="/api/v1/tags")
    app.register_blueprint(submission_bp, url_prefix="/api/v1/submissions")
