from datetime import datetime, timedelta
from random import choice

from bson import ObjectId
from flask import Response, jsonify, abort, request, g
from flask_restful import Resource

import model


class SolveView(Resource):

    def get(self, boothName: str) -> Response:

        booth: model.BoothModel = model.BoothModel.objects(booth_name=boothName).first()
        if not booth:
            return Response('', 204)

        if booth.own_team == g.user.team:
            return Response('', 205)

        if booth.next_capture_time > datetime.now():
            abort(408)

        problem: model.ProblemModel = choice(model.ProblemModel.objects())

        response = {'boothName': boothName,
                    'problemId': str(problem.id),
                    'content': problem.content,
                    'choices': problem.choices}

        return jsonify(response)

    def post(self, boothName: str) -> Response:

        payload: dict = request.json

        problem: model.ProblemModel = model.ProblemModel.objects(id=ObjectId(payload['problemId'])).first()
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
