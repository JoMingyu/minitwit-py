from datetime import timedelta
import os


class Config:
    SERVICE_NAME = 'Minitwit'
    SERVICE_NAME_UPPER = SERVICE_NAME.upper()
    REPRESENTATIVE_HOST = None

    RUN_SETTING = {
        'threaded': True
    }

    SECRET_KEY = os.getenv('SECRET_KEY', '85c145a16bd6f6e1f3e104ca78c6a102')

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=30)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=365)
    JWT_HEADER_TYPE = 'JWT'

    SQLITE_SETTINGS = {
        'database': 'minitwit.db'
    }

    # REDIS_SETTINGS = {
    #     'host': 'localhost',
    #     'port': 6379,
    #     'password': os.getenv('REDIS_PW_{}'.format(SERVICE_NAME_UPPER)),
    #     'db': 0
    # }
