from flask import request
from flask_restful import Resource, abort
from booru.resources import config
from functools import wraps

from flask import current_app as app


def authenticate(func):
    """
    Authenticates an incoming request on the method func.

    :param func: given function or method
    :return: wrapped func
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        if request.headers.get('x-api-key') and request.headers.get('x-api-key') == config["API_KEY"]:
            return func(*args, **kwargs)

        else:
            app.logger.error(f'"GET {request.full_path}" 401')
            abort(401)
    return wrapper


class AuthResource(Resource):
    """
    A Resource that first authenticates an incoming request before using any defined methods.
    """
    method_decorators = [authenticate]
