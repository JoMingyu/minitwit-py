from flask import Blueprint, Response, abort, g
from flask_restful import Api

from app.models.user import UserModel, FollowModel
from app.views import BaseResource, auth_required

api = Api(Blueprint(__name__, __name__))
api.prefix = '/<username>'


@api.resource('/follow')
class Follow(BaseResource):
    @auth_required(UserModel)
    def post(self, username):
        if g.user.username == username:
            abort(400)

        users = UserModel.select().where(UserModel.username == username)

        if not users:
            return Response('', 204)

        user = users[0]

        if FollowModel.select().where( (FollowModel.follower == g.user) & (FollowModel.followee == user) ):
            return Response('', 208)

        FollowModel.insert(follower=g.user, followee=user).execute()

        return Response('', 201)

    @auth_required(UserModel)
    def delete(self, username):
        if g.user.username == username:
            abort(400)

        users = UserModel.select().where(UserModel.username == username)

        if not users:
            return Response('', 204)

        user = users[0]

        FollowModel.delete().where( (FollowModel.follower == g.user) & (FollowModel.followee == user) ).execute()

        return Response('', 200)
