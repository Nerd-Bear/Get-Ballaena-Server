from flask import request, Response
from flask_restful import Resource

from model import UserModel


class AuthView(Resource):

    def get(self, deviceUUID: str) -> Response:
        user = UserModel.get_user_by_device_uuid(device_uuid=deviceUUID)
        if user:
            return Response('', 200)
        return Response('', 204)

    def post(self, deviceUUID: str) -> Response:
        payload: dict = request.json

        user1: UserModel = UserModel.get_user_by_name(name=payload['name'])
        user2: UserModel = UserModel.get_user_by_device_uuid(device_uuid=deviceUUID)
        if any((user1, user2)):
            return Response('exist name or deviceUUID', 205)

        UserModel.create(name=payload['name'], device_uuid=deviceUUID)
        return Response('', 201)
