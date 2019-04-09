from datetime import datetime, timedelta
from random import choice

from flask_restful import Resource
from flasgger import swag_from
from flask import Response, jsonify, abort, request, g

from doc import SOLVE_GET, SOLVE_POST
import model


class SolveView(Resource):

    def _check_time(self, game):
        now: datetime = datetime.now()
        if now < game.start_time:
            abort(406)
        if game.end_time <= now:
            abort(412)

    @swag_from(SOLVE_GET)
    def get(self, boothName: str) -> Response:

        self._check_time(g.game)

        booth: model.BoothModel = model.BoothModel.objects(booth_name=boothName).first()
        if not booth:
            return Response('', 204)

        if booth.own_team == g.user.team:
            return Response('', 205)

        if booth.next_capture_time > datetime.now():
            abort(408)

        problem: model.ProblemModel = choice(model.ProblemModel.objects())

        response = {'boothName': boothName,
                    'problemId': problem.problem_id,
                    'content': problem.content,
                    'choices': problem.choices}

        return jsonify(response)

    @swag_from(SOLVE_POST)
    def post(self, boothName: str) -> Response:

        self._check_time(g.game)

        payload: dict = request.json

        problem: model.ProblemModel = model.ProblemModel.objects(problem_id=payload['problemId']).first()
        booth: model.BoothModel = model.BoothModel.objects(booth_name=boothName).first()
        if not all((problem, booth)):
            return Response('', 204)

        if booth.next_capture_time > datetime.now():
            abort(408)

        if payload['answer'] != problem.answer:
            return Response('', 205)

        booth.own_team = g.user.team
        booth.next_capture_time = datetime.now() + timedelta(minutes=1)
        booth.save()

        return Response('', 201)
