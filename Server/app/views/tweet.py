from flask import Blueprint, Response, abort, g, redirect, url_for, request
from flask_jwt_extended import get_jwt_identity, jwt_optional
from flask_restful import Api

from app.models.tweet import TweetModel
from app.models.user import UserModel
from app.views import BaseResource, auth_required, json_required

api = Api(Blueprint(__name__, __name__))
api.prefix = ''


@api.resource('/tweet')
class Tweet(BaseResource):
    @auth_required(UserModel)
    @json_required({'message': str})
    def post(self):
        payload = request.json

        TweetModel.insert(owner=g.user, message=payload['message']).execute()

        return Response('', 201)


@api.resource('/')
class Index(BaseResource):
    @jwt_optional
    def get(self):
        jwt = get_jwt_identity()

        if jwt:
            # 로그인된 사용자
            users = UserModel.select().where(UserModel.username == jwt)
            if not users:
                abort(401)
            else:
                user = users[0]

                return [{
                    'message': tweet.message,
                    'timestamp': tweet.timestamp
                } for tweet in TweetModel.select().where(TweetModel.owner == user)]
        else:
            return redirect(url_for('app.views.tweet.publictimeline'))


@api.resource('/public-timeline')
class PublicTimeline(BaseResource):
    def get(self):
        return [{
            'owner': tweet.owner.username,
            'message': tweet.message,
            'timestamp': tweet.timestamp
        } for tweet in TweetModel.select().limit(30)]
