from flask import Flask
from flask_cors import CORS

from mongoengine import connect

from config import Config
from view import Router


def create_app(*, test=False) -> Flask:
    app: Flask = Flask(__name__)

    app.config.from_object(Config)

    Router(app).register()
    CORS(app)

    if not test:
        connect('get-terra')

    return app
