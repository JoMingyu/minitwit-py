from functools import wraps
import json
import time

from flask import Response, abort, g, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from werkzeug.exceptions import HTTPException


def after_request(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'deny'

    return response


def exception_handler(e):
    print(e)

    if isinstance(e, HTTPException):
        description = e.description
        code = e.code
    elif isinstance(e, BaseResource.ValidationError):
        description = e.description
        code = 400
    else:
        description = ''
        code = 500

    return jsonify({
        'msg': description
    }), code


def auth_required(model):
    def decorator(fn):
        @wraps(fn)
        @jwt_required
        def wrapper(*args, **kwargs):
            users = model.select().where(model.username == get_jwt_identity())

            if not users:
                abort(401)

            g.user = users[0]

            return fn(*args, **kwargs)
        return wrapper
    return decorator


def json_required(required_keys, check_blank_str=True):
    def decorator(fn):
        if fn.__name__ == 'get':
            print('[WARN] JSON with GET method? on "{}()"'.format(fn.__qualname__))

        @wraps(fn)
        def wrapper(*args, **kwargs):
            if not request.is_json:
                abort(406)

            for key, typ in required_keys.items():
                if key not in request.json or type(request.json[key]) is not typ:
                    abort(400)
                if check_blank_str and typ is str and not request.json[key]:
                    abort(400)

            return fn(*args, **kwargs)
        return wrapper
    return decorator


class BaseResource(Resource):
    def __init__(self):
        self.now = time.strftime('%Y-%m-%d %H:%M:%S')

    @classmethod
    def unicode_safe_json_dumps(cls, data, status_code=200, **kwargs) -> Response:
        return Response(
            json.dumps(data, ensure_ascii=False),
            status_code,
            content_type='application/json; charset=utf8',
            **kwargs
        )

    class ValidationError(Exception):
        def __init__(self, description='', *args):
            self.description = description

            super(BaseResource.ValidationError, self).__init__(*args)


class Router:
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.after_request(after_request)
        app.register_error_handler(Exception, exception_handler)

        from app.views import user
        app.register_blueprint(user.api.blueprint)

        from app.views import tweet
        app.register_blueprint(tweet.api.blueprint)
