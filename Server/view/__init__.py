import os
import threading
import time

from flask import request, Flask
from flask_restful import Api


class Util:

    def reload_server(self):
        time.sleep(2)

        os.system('. ../hook.sh')

    def webhook_event_handler(self):
        if request.headers['X-GitHub-Event'] == 'push':
            threading.Thread(target=self.reload_server).start()

        return 'hello'


class Router(Util):
    def __init__(self, app: Flask):
        self.app = app
        self.api = Api(app)

    def register(self):
        self.app.add_url_rule('/hook', view_func=self.webhook_event_handler, methods=['POST'])

        from view.auth import AuthView
        self.api.add_resource(AuthView, '/auth/<deviceUUID>')

        from view.map import MapView, WebMapView
        self.api.add_resource(MapView, '/map')
        self.api.add_resource(WebMapView, '/map/web')

        from view.solve import SolveView
        self.api.add_resource(SolveView, '/solve/<boothName>')

        from view.team import TeamView
        self.api.add_resource(TeamView, '/team')

        from view.always import AlwaysMapView, AlwaysCaptureView
        self.api.add_resource(AlwaysMapView, '/always/map')
        self.api.add_resource(AlwaysCaptureView, '/always')

        from view.coupon import CouponView
        self.api.add_resource(CouponView, '/coupon')

        from view.ad import AdCaptureView
        self.api.add_resource(AdCaptureView, '/ad')
