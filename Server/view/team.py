from typing import List

from flask_restful import Resource
from flasgger import swag_from
from flask import abort, jsonify, Response, request, g

from doc import TEAM_GET, TEAM_POST
import model


class TeamView(Resource):

    @swag_from(TEAM_GET)
    def get(self) -> Response:
        team_objects: List[model.TeamModel] = model.TeamModel.objects(game=g.game)
        result = {'teamCount': len(team_objects)}

        for team in team_objects:
            result[str(team.team_id)] = {
                'member': [user.user_id for user in model.UserModel.objects(team=team)],
                'teamColor': team.team_color
            }

        return jsonify(result)

    @swag_from(TEAM_POST)
    def post(self) -> Response:
        if not g.user:
            abort(403)

        if g.user.team.team_id != 0:
            return Response('', 204)

        team: model.TeamModel = model.TeamModel.objects(team_id=int(request.args.get('team'))).first()
        if (not team) or len(model.UserModel.objects(team=team)) > 5:
            return Response('', 205)

        g.user.team = team
        g.user.save()

        return Response('', 201)
