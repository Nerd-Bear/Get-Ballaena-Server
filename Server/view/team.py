from flask import jsonify, Response, request, abort
from flask_restful import Resource

from model import TeamModel, UserModel


class TeamView(Resource):

    @staticmethod
    def get_current_user():
        user = UserModel.get_user_by_device_uuid(device_uuid=request.headers['deviceUUID'])
        if user is None:
            return abort(403)
        return user

    def get(self) -> Response:
        teams = TeamModel.get_all_teams()
        result = [{
            'name': team.team_name,
            'member': [user.name for user in UserModel.get_users_by_team(team)],
        } for team in teams]

        return jsonify(result)

    def post(self) -> Response:
        user = self.get_current_user()
        if user.team is not None:
            return Response('', 204)

        team = TeamModel.get_team_by_team_name(team_name=request.json.get('teamName'))
        if team is None:
            return Response('', 205)

        user.team = team
        user.save()

        return Response('', 201)
