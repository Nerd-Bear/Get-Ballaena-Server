from flask_restful import Resource
from flask import jsonify, Response, request, abort

from model import StampModel, CouponModel, UserModel


class StampMapView(Resource):

    @staticmethod
    def get_current_user():
        user = UserModel.get_user_by_device_uuid(device_uuid=request.headers['deviceUUID'])
        if user is None:
            return abort(403)
        return user

    def get(self) -> Response:
        user = self.get_current_user()
        map_: list = []
        stamps = StampModel.get_all_stamps()
        for stamp in stamps:
            map_.append({
                'name': stamp.stamp_name,
                'is_captured': user.is_captured_stamp(stamp=stamp),
                'x': stamp.x,
                'y': stamp.y,
            })

        return jsonify(map_)


class StampCaptureView(Resource):

    @staticmethod
    def get_current_user():
        user = UserModel.get_user_by_device_uuid(device_uuid=request.headers['deviceUUID'])
        if user is None:
            return abort(403)
        return user

    def post(self) -> Response:
        user = self.get_current_user()
        stamp = StampModel.get_stamp_by_stamp_name(request.json['stampName'])
        print(stamp)
        if stamp is None:
            return Response('', 204)
        if user.is_captured_stamp(stamp=stamp):
            return Response('', 205)

        user.capture_stamp(stamp=stamp)
        if user.is_captured_all_stamps():
            CouponModel.create(
                coupon_name='스탬프 이벤트 쿠폰',
                user=user,
            )
            return Response('', 201)
        return Response('', 200)

