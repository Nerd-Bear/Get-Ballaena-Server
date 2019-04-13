from typing import List

from flask_restful import Resource
from flasgger import swag_from
from flask import jsonify, g, Response

from doc import MAP_GET, WEB_MAP_GET
import model


class MapView(Resource):

    @swag_from(MAP_GET)
    def get(self) -> Response:
        map_: dict = {'map': {}, 'myTeam': g.user.team.team_name}
        booths: List[model.BoothModel] = model.BoothModel.objects()

        for booth in booths:
            if booth.own_team is None:
                map_['map'][booth.booth_name] = -1
            elif booth.own_team == g.user.team:
                map_['map'][booth.booth_name] = 1
            else:
                map_['map'][booth.booth_name] = 0

        return jsonify(map_)


class WebMapView(Resource):

    @swag_from(WEB_MAP_GET)
    def get(self) -> Resource:
        booths: List[model.BoothModel] = model.BoothModel.objects()
        map_ = {'map': {}}
        for booth in booths:
            if booth.own_team is None:
                map_['map'][booth.booth_name] = booth.own_team or ''
            else:
                map_['map'][booth.booth_name] = booth.own_team.team_name

        return jsonify(map_)
