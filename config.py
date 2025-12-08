import os


class Config: 
    SECRET_KEY = os.environ.get("SECRET_KEY")
    DEBUG = True


    SQLALCHEMY_DB_URI = os.environ.get("DATABASE_URL")

    SQLALCHEMY_TRACK_MODIFICATIONS = False