from flask import make_response

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
        result = register(data)
        
        if not result:
            return error("User already exists", 400)
        
        # Create response with cookie
        response = make_response(success(
            message="User registered successfully",
            data=result["user"],
            status=201
        ))
        
        # Set cookie
        response.set_cookie(
            key="access_token",
            value=result["access_token"],
            max_age=7*24*60*60,
            path="/",
            secure=False,
            httponly=True,
            samesite="Lax"
        )
        
        return response
    
    except Exception as e:
        return error(str(e))


def login_user(data):
    try:
        result = login(data)
        
        if not result:
            return error("User does not exist", 404)
        
        if result == "Invalid password":
            return error("Invalid password", 401)
        
        # Create response with cookie
        response = make_response(success(
            message="User login successful",
            data=result["user"],
            status=200
        ))
        
        # Set cookie
        response.set_cookie(
        key="access_token",
        value=result["access_token"],
        max_age=7*24*60*60,
        path="/",
        secure=True,  # Must be True for samesite=None on HTTPS
        httponly=True,
        samesite="None"  # Allow cross-site
        )


        print(response.headers, response)
        
        return response
    
    except Exception as e:
        return error(str(e))




