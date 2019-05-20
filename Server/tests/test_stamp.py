from unittest import TestCase
from unittest.mock import MagicMock, patch

from app import create_app
from model import StampModel, UserModel, CouponModel
from tests.request import check_status_code, signup_request, stamp_map_request, stamp_capture_request


def create_stamp_list_mock():
    return [MagicMock(stamp_name=f'stamp {i}', x=i, y=i) for i in range(20)]


def create_user_mock(*, captured_all: bool=False):
    user = MagicMock()
    user.stamps = []
    user.is_captured_stamp = MagicMock(side_effect=is_captured_stamp_side_effect)

    user.is_captured_all_stamps = MagicMock(return_value=captured_all)

    return user


def is_captured_stamp_side_effect(stamp: MagicMock):
    return stamp.x < 10


class StampMapTest(TestCase):

    def setUp(self):
        self.client = create_app(test=True).test_client()

    @patch('view.stamp.StampMapView.get_current_user', return_value=create_user_mock())
    @patch('model.StampModel.get_all_stamps', return_value=create_stamp_list_mock())
    @check_status_code(200)
    def test_success(self,
                     get_all_stamps_mock: MagicMock,
                     get_current_user_mock: MagicMock):
        res = stamp_map_request(self)
        map_ = sorted(res.json, key=lambda x: x['x'])

        get_current_user_mock.assert_called_once_with()
        get_all_stamps_mock.assert_called_once_with()

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
