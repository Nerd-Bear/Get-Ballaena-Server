from unittest import TestCase
from unittest.mock import MagicMock, patch

from bson import ObjectId

from app import create_app
from tests.request import check_status_code, coupon_list_request, coupon_delete_request


def create_coupon_mock_list():
    return [MagicMock(id=i, coupon_name=f'coupon {i}') for i in range(10)]


class TestCouponList(TestCase):

    def setUp(self):
        self.client = create_app(test=True).test_client()

    @patch('view.coupon.CouponView.get_current_user', return_value=MagicMock())
    @patch('model.CouponModel.get_coupons_by_user', return_value=create_coupon_mock_list())
    @check_status_code(200)
    def test_success(self,
                     get_coupons_by_user_mock: MagicMock,
                     get_current_user_mock: MagicMock):
        res = coupon_list_request(self)

        get_current_user_mock.assert_called_once_with()
        get_coupons_by_user_mock.assert_called_once_with(user=get_current_user_mock.return_value)

        for i, coupon in enumerate(res.json):
            expect = {
                'coupon_id': str(i),
                'coupon_name': f'coupon {i}'
            }

            self.assertDictEqual(expect, coupon)

        return res

    @patch('view.coupon.CouponView.get_current_user', return_value=MagicMock())
    @patch('model.CouponModel.get_coupons_by_user', return_value=None)
    @check_status_code(200)
    def test_empty(self,
                   get_coupons_by_user_mock: MagicMock,
                   get_current_user_mock: MagicMock):
        res = coupon_list_request(self)

        get_current_user_mock.assert_called_once_with()
        get_coupons_by_user_mock.assert_called_once_with(user=get_current_user_mock.return_value)

        self.assertEqual(res.json, [])

        return res


class TestCouponRedemption(TestCase):

    def setUp(self):
        self.client = create_app(test=True).test_client()

    @patch('view.coupon.CouponView.get_current_user', return_value=MagicMock())
    @patch('view.coupon.CouponView.get_coupon_id', return_value=ObjectId())
    @patch('model.CouponModel.get_coupon_by_coupon_id_and_user', return_value=MagicMock())
    @check_status_code(200)
    def test_success(self,
                     get_coupon_by_coupon_id_and_user_mock: MagicMock,
                     get_coupon_id_mock: MagicMock,
                     get_current_user_mock: MagicMock):
        res = coupon_delete_request(self)

        get_current_user_mock.assert_called_once_with()
        get_coupon_id_mock.assert_called_once_with()
        get_coupon_by_coupon_id_and_user_mock(
            get_coupon_id_mock.return_value,
            get_current_user_mock.return_value,
        )

        return res

    @patch('view.coupon.CouponView.get_current_user', return_value=MagicMock())
    @patch('view.coupon.CouponView.get_coupon_id', return_value=ObjectId())
    @patch('model.CouponModel.get_coupon_by_coupon_id_and_user', return_value=None)
    @check_status_code(204)
    def test_wrong_coupon_id(self,
                             get_coupon_by_coupon_id_and_user_mock: MagicMock,
                             get_coupon_id_mock: MagicMock,
                             get_current_user_mock: MagicMock):
        res = coupon_delete_request(self)

        get_current_user_mock.assert_called_once_with()
        get_coupon_id_mock.assert_called_once_with()
        get_coupon_by_coupon_id_and_user_mock(
            get_coupon_id_mock.return_value,
            get_current_user_mock.return_value,
        )

        return res

    @patch('view.coupon.CouponView.get_current_user', return_value=MagicMock())
    @patch('view.coupon.CouponView.get_coupon_id', return_value=ObjectId())
    @patch('model.CouponModel.get_coupon_by_coupon_id_and_user', return_value=MagicMock())
    @check_status_code(403)
    def test_wrong_staff_code(self,
                              get_coupon_by_coupon_id_and_user_mock: MagicMock,
                              get_coupon_id_mock: MagicMock,
                              get_current_user_mock: MagicMock):
        res = coupon_delete_request(self, staff_code='wrong')

        get_current_user_mock.assert_called_once_with()
        get_coupon_id_mock.assert_called_once_with()
        get_coupon_by_coupon_id_and_user_mock(
            get_coupon_id_mock.return_value,
            get_current_user_mock.return_value,
        )

        return res
