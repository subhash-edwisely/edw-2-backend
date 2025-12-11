from services.user_service import (
    fetch_all_users, 
    fetch_user_by_id,
    register,
    login,
    fetch_user_progress
)

from utils.response import success, error


def get_all_users():
    try:
        users = fetch_all_users()
        return success(data=users, status=200)
    
    except Exception as e:
        return error(str(e))
    


def get_user(user_id: int):
    try:
        user = fetch_user_by_id(user_id)
        if not user:
            return error("User not found", 404)
        return success(data=user, status=200)
    
    except Exception as e:
        return error(str(e))
    


def register_user(data):
    try:
        user = register(data)
        print("User : ", user)

        
        if not user:
            return error("User already exists")

        return success(data=user, message="User registered successfully", status=200)

    except Exception as e:
        return error(str(e))
    


def login_user(data):
    try:
        user = login(data)
        print("User : ", user)

        if not user:
            return error("User doesnot exist")
    
        if user == "Invalid password":
            return error(user)

        return success(data=user, message="User login successful", status=200)
    
    except Exception as e:
        return error(str(e))

def get_user_progress(user_id: int):
    try:
        progress = fetch_user_progress(user_id)
        if not progress:
            return error("User not found", 404)

        return success(
            data=progress, 
            message="User progress fetched successfully", 
            status=200
        )

    except Exception as e:
        return error(str(e))


