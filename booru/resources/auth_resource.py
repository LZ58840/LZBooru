from flask import request
from flask_restful import Resource, abort
from booru.resources import config
from functools import wraps


def authenticate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if request.headers.get('x-api-key') and request.headers.get('x-api-key') == config["API_KEY"]:
            return func(*args, **kwargs)
        else:
            abort(401)
    return wrapper


class AuthResource(Resource):
    method_decorators = [authenticate]
