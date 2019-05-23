from flask import jsonify, Response, request

from model import TeamModel, UserModel, JoinCodeModel
from view import BaseResource


class TeamView(BaseResource):

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

        join_code = JoinCodeModel.get_join_code_by_code(code=request.json.get('joinCode'))
        if join_code is None:
            return Response('', 205)

        user.team = join_code.team
        user.save()
        join_code.delete()

        return Response('', 201)
