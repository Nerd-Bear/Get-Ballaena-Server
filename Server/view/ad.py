from flask_restful import Resource
from flasgger import swag_from
from flask import g, Response, request

from doc import AD_CAPTURE_GET
import model


class AdCaptureView(Resource):

    @swag_from(AD_CAPTURE_GET)
    def post(self) -> Response:
        ad_name = request.json['adName']
        ad = model.AdQRModel.objects(ad_name=ad_name).first()

        if ad is None:
            return Response('', 204)
        if ad in g.user.always_capture:
            return Response('', 205)

        g.user.always_ad.append(ad)
        g.user.save()
        if len(g.user.ad_capture) == 2:
            model.CouponModel(
                coupon_name='광고 이벤트 쿠폰',
                user=g.user,
            ).save()
            return Response('', 201)
        return Response('', 200)
