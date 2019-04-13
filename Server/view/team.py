from typing import List

from flask_restful import Resource
from flasgger import swag_from
from flask import jsonify, Response

from doc import TEAM_GET
import model


class TeamView(Resource):

    @swag_from(TEAM_GET)
    def get(self) -> Response:
        teams: List[model.TeamModel] = model.TeamModel.objects()
        result = {}
        for team in teams:
            result[team.team_name] = {
                'member': [user.name for user in model.UserModel.objects(team=team)],
            }

        return jsonify(result)
