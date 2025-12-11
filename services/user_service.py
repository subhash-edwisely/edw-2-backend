from models.user import User
from models.college import College
from db import db
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token
from datetime import timedelta


bcrypt = Bcrypt()


def fetch_all_users():
    users = User.query.all()
    return [
        {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "username": user.username,
            "role": user.role.value,
            "total_xp": user.total_xp,
            "created_at": user.created_at,
            "college": user.college.name
        } for user in users
    ]


def fetch_user_by_id(user_id: int):
    user = User.query.get(user_id)
    if not user:
        return None
    
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "username": user.username,
        "role": user.role.value,
        "total_xp": user.total_xp,
        "created_at": user.created_at,
        "college": user.college.name
    }


def register(data: dict):
    name = data.get("name")
    email = data.get("email")
    username = data.get("email")
    password = data.get("password")
    college_name = data.get("college_name")


    user_check_by_email = User.query.filter_by(email=email).first()
    if user_check_by_email:
        return None
    
    user_check_by_username = User.query.filter_by(username=username).first()
    if user_check_by_username:
        return None


    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')


    college = College.query.filter_by(name=college_name).first()
    if not college:
        college = College(
            name=college_name
        )

        db.session.add(college)
        db.session.flush() # college obj ni flush out chestadi


    new_user = User(
        name=name,
        email=email,
        username=username,
        hashed_password=hashed_password,
        college_id = college.id
    )

    db.session.add(new_user)
    db.session.commit()

     # --- Auto-login: create JWT ---
    access_token = create_access_token(
        identity=str(new_user.id),
        expires_delta=timedelta(days=7)
    )

    return {
        "user": {
            "id": new_user.id,
            "name": new_user.name,
            "email": new_user.email,
            "username": new_user.username,
            "role": new_user.role.value,
            "college": new_user.college.name,
            "created_at": new_user.created_at
        },
        "access_token": access_token  # Include token in response
    }



def login(data: dict):
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    if not user:
        return None
    

    doesPasswordMatch = bcrypt.check_password_hash(user.hashed_password, password)
    if not doesPasswordMatch:
        return "Invalid password"


    access_token = create_access_token(
        identity=str(user.id),
        expires_delta=timedelta(days=7)
    )



    return {
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "username": user.username,
            "role": user.role.value,
            "college": user.college.name
        },
        "access_token": access_token  # Include token in response
    }

