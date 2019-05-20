from typing import List

from bson import ObjectId
from flask import jsonify, g, Response, request
from flask_restful import Resource

import model


class CouponView(Resource):

    def get(self):
        result = {'coupons': []}
        coupons: List[model.CouponModel] = model.CouponModel.objects(user=g.user)
        for coupon in coupons:
            result['coupons'].append({
                'coupon_id': str(coupon.id),
                'coupon_name': coupon.coupon_name
            })
        return jsonify(result)

    def delete(self):
        coupon_id = ObjectId(request.args.get('coupon_id'))
        coupon = model.CouponModel.objects(coupon_id=coupon_id, user=g.user).first()
        if coupon is None:
            return Response('', 204)

        coupon.delete()
        return Response('', 200)
