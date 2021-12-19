from flask import request
from flask_restful import Resource, abort
from dotenv import dotenv_values
from functools import wraps


def authenticate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if request.headers.get('x-api-key') and request.headers.get('x-api-key') == "rendersora-x97":
            return func(*args, **kwargs)
        else:
            abort(401)
    return wrapper


class AuthResource(Resource):
    method_decorators = [authenticate]
