from bson import ObjectId
from flask import jsonify, Response, request, abort

from const import STAFF_CODE
from model import CouponModel
from view import BaseResource


class CouponView(BaseResource):

    @staticmethod
    def get_coupon_id():
        try:
            return ObjectId(request.json.get('couponId'))
        except:
            abort(400)

    def get(self):
        user = self.get_current_user()
        coupons = CouponModel.get_coupons_by_user(user=user)
        result = [{'coupon_id': str(coupon.id), 'coupon_name': coupon.coupon_name} for coupon in coupons or []]
        return jsonify(result)

    def delete(self):
        user = self.get_current_user()
        coupon_id = self.get_coupon_id()
        coupon = CouponModel.get_coupon_by_coupon_id_and_user(coupon_id, user)
        if coupon is None:
            return Response('', 204)

        if request.json.get('staffCode') != STAFF_CODE:
            abort(403)

        coupon.delete()
        return Response('', 200)
