from flask import Flask
from flask_jwt_extended import JWTManager
# from redis import Redis


def create_app(*config_cls) -> Flask:
    print('[INFO] Flask application initialized with {}'.format([config.__name__ for config in config_cls]))

    app_ = Flask(__name__)

    for config in config_cls:
        app_.config.from_object(config)

    JWTManager().init_app(app_)

    return app_
