from flask import Flask
from flask_jwt_extended import JWTManager

from app.views import Router


def create_app(*config_cls) -> Flask:
    print('[INFO] Flask application initialized with {}'.format([config.__name__ for config in config_cls]))

    app_ = Flask(__name__)

    for config in config_cls:
        app_.config.from_object(config)

    JWTManager().init_app(app_)
    Router().init_app(app_)

    from app.models import db, user, tweet
    db.create_tables([user.UserModel, tweet.TweetModel])

    return app_
