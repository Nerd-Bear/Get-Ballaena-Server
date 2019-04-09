from typing import List

from flask_restful import Resource
from flasgger import swag_from
from flask import abort, jsonify, Response, request, g

from doc import TEAM_GET, TEAM_POST
import model


class TeamView(Resource):

    @swag_from(TEAM_GET)
    def get(self) -> Response:
        teams: List[model.TeamModel] = model.TeamModel.objects()
        result = {}
        for team in teams:
            result[team.team_name] = {
                'member': [user.user_id for user in model.UserModel.objects(team=team)],
            }

        return jsonify(result)

    @swag_from(TEAM_POST)
    def post(self) -> Response:
        if not g.user:
            abort(403)

        if g.user.team is not None:
            return Response('', 204)

        team: model.TeamModel = model.TeamModel.objects(team_name=request.json['teamName']).first()
        if not team:
            return Response('', 205)

        g.user.team = team
        g.user.save()

        return Response('', 201)
