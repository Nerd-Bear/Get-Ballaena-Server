from typing import List

from flask_restful import Resource
from flask import jsonify, g, Response

import model


class MapView(Resource):

    def get(self) -> Response:
        map_: dict = {'map': {}, 'myTeam': g.user.team.team_name}
        booths: List[model.BoothModel] = model.BoothModel.objects()

        for booth in booths:
            if booth.own_team is None:
                value = -1
            elif booth.own_team == g.user.team:
                value = 1
            else:
                value = 0
            map_['map'][booth.booth_name] = {
                'team': value,
                'latitude': booth.latitude,
                'longitude': booth.longitude,
            }

        return jsonify(map_)


class WebMapView(Resource):

    def get(self) -> Resource:
        booths: List[model.BoothModel] = model.BoothModel.objects()
        map_ = {'map': {}}
        for booth in booths:
            map_['map'][booth.booth_name] = {
                'teamName': '' if booth.own_team is None else booth.own_team.team_name,
                'latitude': booth.latitude,
                'longitude': booth.longitude,
            }

        return jsonify(map_)
