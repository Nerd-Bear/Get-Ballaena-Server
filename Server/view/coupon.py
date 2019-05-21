from bson import ObjectId
from flask import jsonify, Response, request, abort

from view import BaseResource
from model import CouponModel


class CouponView(BaseResource):

    @staticmethod
    def get_coupon_id():
        try:
            return ObjectId(request.args.get('coupon_id'))
        except:
            abort(400)

    def get(self):
        user = self.get_current_user()
        coupons = CouponModel.get_coupons_by_user(user=user)

        result = [{'coupon_id': str(coupon.id), 'coupon_name': coupon.coupon_name}for coupon in coupons or []]
        return jsonify(result)

    def delete(self):
        user = self.get_current_user()
        coupon_id = self.get_coupon_id()
        coupon = CouponModel.get_coupon_by_coupon_id_and_user(coupon_id, user)
        if coupon is None:
            return Response('', 204)

        coupon.delete()
        return Response('', 200)
