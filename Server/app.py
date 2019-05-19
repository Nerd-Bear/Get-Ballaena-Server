from flask import Flask, request, g, abort
from flask_cors import CORS

from mongoengine import connect

from config import Config
from view import Router
from model import UserModel


def set_g_user():
    if 'deviceUUID' in request.headers:
        g.user = UserModel.objects(device_uuid=request.headers['deviceUUID']).first()
        if g.user is None:
            return abort(403)


def create_app(*, test=False) -> Flask:
    app: Flask = Flask(__name__)

    app.config.from_object(Config)
    Router(app).register()
    app.before_request(set_g_user)

    CORS(app)

    if not test:
        connect('get-terra')

    return app
