from datetime import datetime, timedelta

from flask import Flask, abort, request, current_app, Response
from flask_restful import Api, Resource

import model
from const import ADMIN_CODE


class Router:
    def __init__(self, app: Flask):
        self.app = app
        self.api = Api(app)

    def register(self):
        from view.auth import AuthView
        self.api.add_resource(AuthView, '/auth/<deviceUUID>')

        from view.map import MapView, WebMapView
        self.api.add_resource(MapView, '/map')
        self.api.add_resource(WebMapView, '/map/web')

        from view.solve import SolveView
        self.api.add_resource(SolveView, '/solve/<boothName>')

        from view.team import TeamView, TeamCheckView
        self.api.add_resource(TeamView, '/team')
        self.api.add_resource(TeamCheckView, '/team/check')

        from view.stamp import StampCaptureView, StampMapView
        self.api.add_resource(StampMapView, '/stamp/map')
        self.api.add_resource(StampCaptureView, '/stamp')

        from view.coupon import CouponView
        self.api.add_resource(CouponView, '/coupon')

        self.app.add_url_rule('/admin/initialize', 'initialize', view_func=initialize, methods=['POST'])
        self.app.add_url_rule('/admin/start', 'start_game', view_func=start_game, methods=['POST'])


def get_all_models():
    return [getattr(model, m) for m in dir(model) if m.endswith('Model')]


def initialize():
    admin_code = request.json.get('adminCode')
    if admin_code != ADMIN_CODE:
        return abort(403)

    models = get_all_models()
    for m in models:
        m.initialize()

    return Response('', 201)


def start_game():
    admin_code = request.json.get('adminCode')
    if admin_code != ADMIN_CODE:
        return abort(403)
    current_app.config['START_TIME'] = BaseResource.get_kst_now()
    current_app.config['END_TIME'] = BaseResource.get_kst_now() + timedelta(minutes=30)

    return Response('', 201)


class BaseResource(Resource):

    @staticmethod
    def get_kst_now():
        return datetime.utcnow() + timedelta(hours=9)

    @staticmethod
    def get_start_time() -> datetime:
        return current_app.config['START_TIME']

    @staticmethod
    def get_end_time() -> datetime:
        return current_app.config['END_TIME']

    def check_time(self):
        start_time = self.get_start_time()
        now = self.get_kst_now()
        end_time = self.get_end_time()

        if now < start_time:
            abort(406)
        elif end_time < now:
            abort(408)

    def get_left_time(self):
        left_time = self.get_end_time() - self.get_kst_now()
        minutes = left_time.seconds // 60
        seconds = left_time.seconds % 60
        return f'{minutes}:{seconds}'

    @staticmethod
    def get_current_user():
        user = model.UserModel.get_user_by_device_uuid(device_uuid=request.headers.get('deviceUUID'))
        if user is None:
            return abort(403)
        return user
