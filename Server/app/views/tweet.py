from flask import Blueprint, Response, abort, g, redirect, url_for, request
from flask_jwt_extended import get_jwt_identity, jwt_optional
from flask_restful import Api

from app.models.tweet import TweetModel
from app.models.user import FollowModel, UserModel
from app.views import BaseResource, auth_required, json_required

api = Api(Blueprint(__name__, __name__))
api.prefix = ''


def extract_tweet_data(tweet):
    return {
        'message': tweet.message,
        'timestamp': tweet.timestamp
    }


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

                return [extract_tweet_data(tweet) for tweet in TweetModel.select().where(TweetModel.owner == user)]
        else:
            return redirect(url_for('app.views.tweet.publictimeline'))


@api.resource('/timeline/<username>')
class UserTimeline(BaseResource):
    @auth_required(UserModel)
    def get(self, username):
        users = UserModel.select().where(UserModel.username == username)

        if not users:
            abort(404)

        user = users[0]

        return {
            'following': bool(FollowModel.select().where( (FollowModel.follower == g.user) & (FollowModel.followee == user) )),
            'tweets': [extract_tweet_data(tweet) for tweet in TweetModel.select().where(TweetModel.owner == username)]
        }


@api.resource('/public-timeline')
class PublicTimeline(BaseResource):
    def get(self):
        return [dict(
            extract_tweet_data(tweet),
            **{'owner': tweet.owner.username}
        ) for tweet in TweetModel.select().limit(30)]
