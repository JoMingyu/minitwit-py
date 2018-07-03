from flask import Blueprint, Response, g, request
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
