from flask_restful import Resource
from flasgger import swag_from
from flask import request, Response

from doc import AUTH_POST, CHECK_DEVICE_UUID_GET
import model


class AuthView(Resource):

    @swag_from(CHECK_DEVICE_UUID_GET)
    def get(self, deviceUUID: str) -> Response:
        user = model.UserModel.objects(device_uuid=deviceUUID).first()
        if user is None:
            return Response('', 200)
        return Response('', 204)

    @swag_from(AUTH_POST)
    def post(self, deviceUUID: str) -> Response:
        payload: dict = request.json

        user1: model.UserModel = model.UserModel.objects(name=payload['name']).first()
        user2: model.UserModel = model.UserModel.objects(device_uuid=deviceUUID).first()
        if not all((user1, user2)):
            return Response('exist name or deviceUUID', 205)

        model.UserModel(name=payload['name'], device_uuid=deviceUUID).save()
        return Response('', 201)
