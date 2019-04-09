from flask import Flask
from flask_cors import CORS
from flasgger import Swagger

from mongoengine import connect

from config import Config
from view import Router


def create_app() -> Flask:
    app: Flask = Flask(__name__)

    app.config.from_object(Config)
    Router(app).register()
    CORS(app)

    connect('get-terra')

    Swagger(app, template=app.config['SWAGGER_TEMPLATE'])
    return app
