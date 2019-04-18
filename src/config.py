# config.py

import os


class Development:

    DEBUG = True
    TESTING = False
    JWT_SECRET_KEY = os.environ['JWT_SECRET_KEY']
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']


class Production:

    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    JWT_SECRET_KEY = os.environ['JWT_SECRET_KEY']


app_config = {
    'development': Development,
    'production': Production
}

