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
