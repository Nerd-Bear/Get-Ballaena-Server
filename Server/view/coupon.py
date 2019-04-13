from bson import ObjectId
from typing import List

from flask_restful import Resource
from flasgger import swag_from
from flask import jsonify, g, Response, request

from doc import COUPON_GET, COUPON_DELETE
import model


class CouponView(Resource):

    @swag_from(COUPON_GET)
    def get(self):
        result = {'coupons': []}
        coupons: List[model.CouponModel] = model.CouponModel(user=g.user)
        for coupon in coupons:
            result['coupons'].append({
                'coupon_id': str(coupon.id),
                'coupon_name': coupon.coupon_name
            })
        return jsonify(result)

    @swag_from(COUPON_DELETE)
    def delete(self):
        coupon_id = ObjectId(request.args.get('coupon_id'))
        coupon = model.CouponModel.objects(coupon_id=coupon_id, user=g.user).first()
        if coupon is None:
            return Response('', 204)

        coupon.delete()
        return Response('', 200)
