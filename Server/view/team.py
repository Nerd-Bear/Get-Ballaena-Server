from typing import List

from flask_restful import Resource
from flask import jsonify, Response, request, g

import model


class TeamView(Resource):

    def get(self) -> Response:
        teams: List[model.TeamModel] = model.TeamModel.objects()
        result = {}
        for team in teams:
            result[team.team_name] = {
                'member': [user.name for user in model.UserModel.objects(team=team)],
            }

        return jsonify(result)

    def post(self) -> Response:
        if g.user.team is not None:
            return Response('', 204)

        team: model.TeamModel = model.TeamModel.objects(team_name=request.json.get('teamName')).first()
        if team is None:
            return Response('', 205)

        g.user.team = team
        g.user.save()

        return Response('', 201)
