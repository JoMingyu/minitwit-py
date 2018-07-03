from flask import Blueprint, Response, abort, g, request
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_restful import Api

from werkzeug.security import check_password_hash, generate_password_hash

from app.models.user import UserModel
from app.views import BaseResource, json_required

api = Api(Blueprint(__name__, __name__))
api.prefix = ''


@api.resource('/signup')
class Signup(BaseResource):
    @json_required({'username': str, 'email': str, 'pw': str})
    def post(self):
        payload = request.json

        username = payload['username']
        email = payload['email']
        pw = payload['pw']
        pw_hash = generate_password_hash(pw)

        if UserModel.select().where( (UserModel.username == username) | (UserModel.email == email) ):
            abort(409)

        UserModel.insert(username=username, email=email, pw_hash=pw_hash).execute()

        return Response('', 201)


@api.resource('/login')
class Login(BaseResource):
    @json_required({'username': str, 'pw': str})
    def post(self):
        payload = request.json

        username = payload['username']
        pw = payload['pw']

        users = UserModel.select().where(UserModel.username == username)

        if not users:
            abort(401)
        else:
            user = users[0]

            if check_password_hash(user.pw_hash, pw):
                return {
                    'accessToken': create_access_token(username),
                    'refreshToken': create_refresh_token(username)
                }
            else:
                abort(401)
