from flask_restful import Resource
from flask import request, Response

import model


class AuthView(Resource):

    def get(self, deviceUUID: str) -> Response:
        user = model.UserModel.objects(device_uuid=deviceUUID).first()
        if user:
            return Response('', 200)
        return Response('', 204)

    def post(self, deviceUUID: str) -> Response:
        payload: dict = request.json

        user1: model.UserModel = model.UserModel.objects(name=payload['name']).first()
        user2: model.UserModel = model.UserModel.objects(device_uuid=deviceUUID).first()
        if any((user1, user2)):
            return Response('exist name or deviceUUID', 205)

        model.UserModel(name=payload['name'], device_uuid=deviceUUID).save()
        return Response('', 201)
