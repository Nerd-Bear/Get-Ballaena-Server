from typing import List

from flask import jsonify, Response, request, g
from flask_restful import Resource

import model


class TeamView(Resource):

    def get_current_user(self):
        return g.user

    def get_team(self, team_name: str):
        return model.TeamModel.objects(team_name=team_name).first()

    def get(self) -> Response:
        teams: List[model.TeamModel] = model.TeamModel.objects()
        result = [{
            'name': team.team_name,
            'member': [user.name for user in model.UserModel.objects(team=team)],
        } for team in teams]

        return jsonify(result)

    def post(self) -> Response:
        current_user = self.get_current_user()
        if current_user.team is not None:
            return Response('', 204)

        team = self.get_team(team_name=request.json.get('teamName'))
        if team is None:
            return Response('', 205)

        current_user.team = team
        current_user.save()

        return Response('', 201)
