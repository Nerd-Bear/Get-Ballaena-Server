from flask import Flask, abort, request
from flask_restful import Api, Resource

from model import UserModel


class BaseResource(Resource):

    @staticmethod
    def get_current_user():
        user = UserModel.get_user_by_device_uuid(device_uuid=request.headers['deviceUUID'])
        if user is None:
            return abort(403)
        return user


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

        from view.team import TeamView
        self.api.add_resource(TeamView, '/team')

        from view.stamp import StampCaptureView, StampMapView
        self.api.add_resource(StampMapView, '/stamp/map')
        self.api.add_resource(StampCaptureView, '/stamp')

        from view.coupon import CouponView
        self.api.add_resource(CouponView, '/coupon')
