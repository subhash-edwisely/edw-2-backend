import os


class Config: 

    # print(os.environ.get("DATABASE_URL"))

    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")  # used to sign JWTs
    JWT_TOKEN_LOCATION = ["cookies"]                   # read JWT from cookies
    JWT_ACCESS_COOKIE_NAME = "access_token"           # cookie name
    JWT_COOKIE_SECURE = False                          # True if using HTTPS
    JWT_COOKIE_SAMESITE = "Lax"                        # CSRF protection
    JWT_COOKIE_CSRF_PROTECT = False 


    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False