from flask import Flask, request, g
from flask_cors import CORS
from flasgger import Swagger

from mongoengine import connect

from config import Config
from view import Router
from model import UserModel


def set_g_user():
    if 'deviceUUID' in request.headers:
        g.user = UserModel.objects(device_uuid=request.headers['deviceUUID'])


def create_app() -> Flask:
    app: Flask = Flask(__name__)

    app.config.from_object(Config)
    Router(app).register()
    app.before_request(set_g_user)

    CORS(app)
    connect('get-terra')

    Swagger(app, template=app.config['SWAGGER_TEMPLATE'])
    return app
