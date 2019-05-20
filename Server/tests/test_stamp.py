from unittest import TestCase
from unittest.mock import MagicMock, patch

from app import create_app
from tests.request import check_status_code, stamp_map_request, stamp_capture_request


def create_stamp_list_mock():
    return [MagicMock(stamp_name=f'stamp {i}', x=i, y=i) for i in range(20)]


def create_user_mock(*, captured_stamp: bool=False, captured_all: bool=False, captured_half: bool=False):
    user = MagicMock()
    user.stamps = []

    if captured_half:
        user.is_captured_stamp.side_effect = is_captured_stamp_side_effect
    else:
        user.is_captured_stamp = MagicMock(return_value=captured_stamp)

    user.is_captured_all_stamps = MagicMock(return_value=captured_all)

    return user


def is_captured_stamp_side_effect(stamp: MagicMock):
    return stamp.x < 10


class StampMapTest(TestCase):

    def setUp(self):
        self.client = create_app(test=True).test_client()

    @patch('view.stamp.StampMapView.get_current_user', return_value=create_user_mock(captured_half=True))
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


class StampCaptureTest(TestCase):

    def setUp(self):
        self.client = create_app(test=True).test_client()

    @patch('view.stamp.StampCaptureView.get_current_user', return_value=create_user_mock())
    @patch('model.StampModel.get_stamp_by_stamp_name', return_Value=MagicMock())
    @check_status_code(200)
    def test_success(self,
                     get_stamp_by_stamp_name_mock: MagicMock,
                     get_current_user_mock: MagicMock):
        res = stamp_capture_request(self)

        get_current_user_mock.assert_called_once_with()
        get_stamp_by_stamp_name_mock.assert_called_once_with('stamp 0')

        return res

    @patch('view.stamp.StampCaptureView.get_current_user', return_value=create_user_mock(captured_stamp=True))
    @patch('model.StampModel.get_stamp_by_stamp_name', return_Value=MagicMock())
    @check_status_code(205)
    def test_already_captured(self,
                              get_stamp_by_stamp_name_mock: MagicMock,
                              get_current_user_mock: MagicMock):
        res = stamp_capture_request(self)

        get_current_user_mock.assert_called_once_with()
        get_stamp_by_stamp_name_mock.assert_called_once_with('stamp 0')

        return res

    @patch('view.stamp.StampCaptureView.get_current_user', return_value=create_user_mock())
    @patch('model.StampModel.get_stamp_by_stamp_name', return_value=None)
    @check_status_code(204)
    def test_bad_booth_name(self,
                            get_stamp_by_stamp_name_mock: MagicMock,
                            get_current_user_mock: MagicMock):
        res = stamp_capture_request(self)

        get_current_user_mock.assert_called_once_with()
        get_stamp_by_stamp_name_mock.assert_called_once_with('stamp 0')

        return res

    @patch('view.stamp.StampCaptureView.get_current_user', return_value=create_user_mock(captured_all=True))
    @patch('model.StampModel.get_stamp_by_stamp_name', return_value=MagicMock())
    @patch('model.CouponModel.create', return_value=MagicMock())
    @check_status_code(201)
    def test_create_stamp_coupon(self,
                                 coupon_model_create_mock: MagicMock,
                                 get_stamp_by_stamp_name_mock: MagicMock,
                                 get_current_user_mock: MagicMock):
        res = stamp_capture_request(self)

        get_current_user_mock.assert_called_once_with()
        get_stamp_by_stamp_name_mock.assert_called_once_with('stamp 0')
        coupon_model_create_mock.assert_called_once_with(
            coupon_name='스탬프 이벤트 쿠폰',
            user=get_current_user_mock.return_value
        )

        return res
