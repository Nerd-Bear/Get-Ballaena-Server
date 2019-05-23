from flask import Response, jsonify, request, make_response

from model import BoothModel, ProblemModel
from view import BaseResource


class SolveView(BaseResource):

    def get_left_delay(self, booth: BoothModel):
        left_delay = booth.next_capture_time - self.get_kst_now()
        minute = left_delay.seconds // 60
        second = left_delay.seconds % 60
        return f'{minute}:{second}'

    def is_booth_captured_by_user_team(self, booth: BoothModel):
        return self.get_current_user().team == booth.own_team

    def is_in_delay(self, booth: BoothModel):
        return booth.next_capture_time > self.get_kst_now()

    def get(self, boothName: str) -> Response:
        self.check_time()

        booth = BoothModel.get_booth_by_booth_name(booth_name=boothName)
        if not booth:
            return Response('', 204)

        if self.is_booth_captured_by_user_team(booth=booth):
            return Response('', 205)

        if self.is_in_delay(booth=booth):
            return make_response(
                jsonify({
                    'delayTime': self.get_left_delay(booth=booth)
                }), 409
            )

        problem = ProblemModel.get_random_problem()

        response = {'boothName': boothName,
                    'problemId': str(problem.id),
                    'content': problem.content,
                    'choices': problem.choices}

        return jsonify(response)

    def post(self, boothName: str) -> Response:

        payload: dict = request.json

        problem = ProblemModel.get_problem_by_id(id=payload['problemId'])
        booth = BoothModel.get_booth_by_booth_name(booth_name=boothName)
        if not all((problem, booth)):
            return Response('', 204)

        if self.is_in_delay(booth=booth):
            return make_response(
                jsonify({
                    'delayTime': self.get_left_delay(booth=booth)
                }), 409
            )

        if payload['answer'] != problem.answer:
            booth.set_delay(minutes=1)
            return Response('', 205)

        booth.capture(user=self.get_current_user())

        return Response('', 201)
