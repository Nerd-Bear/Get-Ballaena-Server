from unittest import TestCase

from app import create_app
from model import StampModel, UserModel, CouponModel
from tests.request import check_status_code, signup_request, stamp_map_request, stamp_capture_request


class StampMapTest(TestCase):

    def setUp(self):
        self.client = create_app(test=True).test_client()
        signup_request(self)

        user: UserModel = UserModel.objects(name='test').first()

        for i in range(10):
            stamp = StampModel(stamp_name=f'stamp {i}', x=i, y=i).save()
            user.stamps.append(stamp)
        user.save()

        for i in range(10, 20):
            StampModel(stamp_name=f'stamp {i}', x=i, y=i).save()

    def tearDown(self):
        StampModel.drop_collection()
        UserModel.drop_collection()

    @check_status_code(200)
    def test_success(self):
        res = stamp_map_request(self)
        map_ = sorted(res.json, key=lambda x: x['x'])

        for i, stamp in enumerate(map_):
            expect = {
                'name': f'stamp {i}',
                'is_captured': i < 10,
                'x': i,
                'y': i
            }
            self.assertDictEqual(expect, stamp)
        return res

    @check_status_code(403)
    def test_wrong_deviceUUID(self):
        return stamp_map_request(self, device_uuid='wrong')


class StampCaptureTest(TestCase):

    def setUp(self):
        self.client = create_app(test=True).test_client()
        signup_request(self)

        for i in range(20):
            StampModel(stamp_name=f'stamp {i}', x=i, y=i).save()

    def tearDown(self):
        StampModel.drop_collection()
        UserModel.drop_collection()

    @check_status_code(200)
    def test_success(self):
        return stamp_capture_request(self)

    @check_status_code(205)
    def test_already_captured(self):
        stamp_capture_request(self)
        return stamp_capture_request(self)

    @check_status_code(204)
    def test_bad_booth_name(self):
        return stamp_capture_request(self, stamp_name='wrong')

    @check_status_code(201)
    def test_create_stamp_coupon(self):
        for i in range(19):
            stamp_capture_request(self, stamp_name=f'stamp {i}')
        res = stamp_capture_request(self, stamp_name=f'stamp 19')

        user: UserModel = UserModel.objects(name='test').first()
        self.assertTrue(CouponModel.objects(user=user, coupon_name='스탬프 이벤트 쿠폰').first())
        return res
