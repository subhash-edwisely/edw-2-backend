from flask import Flask
from config import Config
from db import db
# from routes import register_routes


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)


    # This must be called before accessing the database engine or session with the app.
    db.init_app(app)

    # register_routes(app)


    with app.app_context():
        # Create tables that do not exist in the database
        import models
        db.create_all()
    

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000)