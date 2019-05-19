from typing import List

from flask_restful import Resource
from flask import jsonify, g, Response, request

import model


class StampMapView(Resource):

    def get(self) -> Response:
        map_: list = []
        stamps: List[model.StampModel] = model.StampModel.objects()

        for stamp in stamps:
            map_.append({
                'name': stamp.stamp_name,
                'is_captured': stamp in g.user.stamps,
                'x': stamp.x,
                'y': stamp.y,
            })

        return jsonify(map_)


class StampCaptureView(Resource):

    def post(self) -> Response:
        stamp_name = request.json['stampName']
        stamp = model.StampModel.objects(stamp_name=stamp_name).first()

        if stamp is None:
            return Response('', 204)
        if stamp in g.user.stamps:
            return Response('', 205)

        g.user.stamps.append(stamp)
        g.user.save()
        if len(g.user.stamps) == len(model.StampModel.objects):
            model.CouponModel(
                coupon_name='스탬프 이벤트 쿠폰',
                user=g.user,
            ).save()
            return Response('', 201)
        return Response('', 200)

