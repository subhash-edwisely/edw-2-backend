from flask import jsonify


def success(message="Success", data=None, status=200):
    
    response = {
        "success": True,
        "message": message
    }

    if data is not None:
        response["data"] = data

    return jsonify(response), status





def error(message="Something went wrong", status=500, errors=None):
    
    response = {
        "success": False,
        "message": message
    }

    if errors is not None:
        response["errors"] = errors

    
    return jsonify(response), status
