from typing import List

from flask_restful import Resource
from flasgger import swag_from
from flask import jsonify, g, Response

from doc import MAP_GET
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
