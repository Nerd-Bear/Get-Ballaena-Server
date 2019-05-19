from flask import jsonify, Response, request, g
from flask_restful import Resource

from model import TeamModel, UserModel


class TeamView(Resource):

    def get_current_user(self):
        return g.user

    def get(self) -> Response:
        teams = TeamModel.get_all_teams()
        result = [{
            'name': team.team_name,
            'member': [user.name for user in UserModel.get_users_by_team(team)],
        } for team in teams]

        return jsonify(result)

    def post(self) -> Response:
        current_user = self.get_current_user()
        if current_user.team is not None:
            return Response('', 204)

        team = TeamModel.get_team_by_team_name(team_name=request.json.get('teamName'))
        if team is None:
            return Response('', 205)

        current_user.team = team
        current_user.save()

        return Response('', 201)
