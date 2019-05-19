from unittest import TestCase
from unittest.mock import MagicMock, patch

from app import create_app
from tests.request import check_status_code, signup_request, signin_request


class SignupTest(TestCase):

    def setUp(self):
        self.client = create_app(test=True).test_client()

    @check_status_code(201)
    @patch('model.UserModel.create', return_value=MagicMock())
    @patch('model.UserModel.get_user_by_device_uuid', return_value=None)
    @patch('model.UserModel.get_user_by_name', return_value=None)
    def test_signup_success(self,
                            get_user_by_name_mock: MagicMock,
                            get_user_by_device_uuid_mock: MagicMock,
                            create_mock: MagicMock):
        res = signup_request(self)
        get_user_by_name_mock.assert_called_once_with(name='test')
        get_user_by_device_uuid_mock.assert_called_once_with(device_uuid='test')
        create_mock.assert_called_once_with(name='test', device_uuid='test')
        return res

    @check_status_code(205)
    @patch('model.UserModel.get_user_by_device_uuid', return_value=None)
    @patch('model.UserModel.get_user_by_name', return_value=MagicMock())
    def test_exist_name(self,
                        get_user_by_name_mock: MagicMock,
                        get_user_by_device_uuid_mock: MagicMock):
        res = signup_request(self)
        get_user_by_name_mock.assert_called_once_with(name='test')
        get_user_by_device_uuid_mock.assert_called_once_with(device_uuid='test')
        return res

    @check_status_code(205)
    @patch('model.UserModel.get_user_by_device_uuid', return_value=MagicMock())
    @patch('model.UserModel.get_user_by_name', return_value=None)
    def test_exist_deviceUUID(self,
                              get_user_by_name_mock: MagicMock,
                              get_user_by_device_uuid_mock: MagicMock):
        res = signup_request(self)
        get_user_by_name_mock.assert_called_once_with(name='test')
        get_user_by_device_uuid_mock.assert_called_once_with(device_uuid='test')
        return res


class SigninTest(TestCase):

    def setUp(self):
        self.client = create_app(test=True).test_client()

    @check_status_code(200)
    @patch('model.UserModel.get_user_by_device_uuid', return_value=MagicMock())
    def test_success_signin(self,
                            get_user_by_device_uuid_mock: MagicMock):
        res = signin_request(self)
        get_user_by_device_uuid_mock.assert_called_once_with(device_uuid='test')
        return res

    @check_status_code(204)
    @patch('model.UserModel.get_user_by_device_uuid', return_value=None)
    def test_fail_signin(self,
                         get_user_by_device_uuid_mock: MagicMock):
        res = signin_request(self)
        get_user_by_device_uuid_mock.assert_called_once_with(device_uuid='test')
        return res
