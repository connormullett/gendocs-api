# src/app.py

from flask import Flask
from flask_cors import CORS
from flask_heroku import Heroku
from .config import app_config
from .models import db, bcrypt

from .views.user_view import user_api
from .views.doc_view import doc_api
from .views.comment_view import comment_api


def create_app(env_name):
    app = Flask(__name__)

    app.config.from_object(app_config[env_name])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    CORS(app)
    heroku = Heroku(app)

    app.register_blueprint(user_api, url_prefix='/v1/users')
    app.register_blueprint(doc_api, url_prefix='/v1/docs')
    app.register_blueprint(comment_api, url_prefix='/v1/comments')

    bcrypt.init_app(app)
    db.init_app(app)

    return app

