from typing import List

from flask_restful import Resource
from flasgger import swag_from
from flask import jsonify, g, Response, request

from doc import ALWAYS_MAP_GET, ALWAYS_CAPTURE_GET
import model


class AlwaysMapView(Resource):

    @swag_from(ALWAYS_MAP_GET)
    def get(self) -> Response:
        map_: dict = {'map': {}}
        booths: List[model.AlwaysBoothModel] = model.AlwaysBoothModel.objects()

        for booth in booths:
            map_['map'][booth.booth_name] = {
                'captured': booth in g.user.always_capture,
                'latitude': booth.latitude,
                'longitude': booth.longitude,
            }

        return jsonify(map_)


class AlwaysCaptureView(Resource):

    @swag_from(ALWAYS_CAPTURE_GET)
    def get(self) -> Response:
        booth_name = request.json['boothName']
        booth = model.AlwaysBoothModel.objects(booth_name=booth_name).first()

        if booth is None:
            return Response('', 204)
        if booth in g.user.always_capture:
            return Response('', 205)

        g.user.always_capture.append(booth)
        g.user.save()
        if len(g.user.always_capture) == len(model.AlwaysBoothModel.objects):
            model.CouponModel(
                coupon_name='상시 이벤트 쿠폰',
                user=g.user,
            ).save()
            return Response('', 201)
        return Response('', 200)

