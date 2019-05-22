from flask import jsonify, Response

from model import BoothModel
from view import BaseResource


class MapView(BaseResource):

    @staticmethod
    def get_team_name():
        user = MapView.get_current_user()
        return user.team.team_name

    def get(self) -> Response:
        self.check_time()

        map_ = {
            'map': [],
            'myTeam': self.get_team_name(),
            'leftTime': self.get_left_time(),
        }

        booths = BoothModel.get_all_booths()
        for booth in booths:
            map_['map'].append({
                'booth_name': booth.booth_name,
                'own_team': booth.own_team.team_name or '',
                'x': booth.x,
                'y': booth.y,
            })

        return jsonify(map_)
