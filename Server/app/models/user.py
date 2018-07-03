from peewee import *

from app.models import db


class UserModel(Model):
    username = CharField(
        max_length=50,
        primary_key=True
    )

    email = CharField(
        max_length=100,
        unique=True
    )

    pw_hash = TextField()

    class Meta:
        database = db


class FollowModel(Model):
    follower = ForeignKeyField(
        model=UserModel,
        on_delete='CASCADE',
        on_update='CASCADE'
    )

    followee = ForeignKeyField(
        model=UserModel,
        on_delete='CASCADE',
        on_update='CASCADE'
    )

    class Meta:
        database = db
