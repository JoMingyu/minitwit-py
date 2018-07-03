from time import time

from peewee import *

from app.models import db
from app.models.user import UserModel


class TweetModel(Model):
    owner = ForeignKeyField(
        model=UserModel,
        on_delete='CASCADE',
        on_update='CASCADE'
    )

    message = TextField()
    timestamp = TimeField(
        default=time
    )

    class Meta:
        database = db
