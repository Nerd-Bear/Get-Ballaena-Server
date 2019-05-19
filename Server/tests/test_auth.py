from unittest import TestCase
from unittest.mock import MagicMock, patch

from app import create_app
from model import UserModel

from tests.request import check_status_code, signup_request, signin_reqeust


class SignupTest(TestCase):

    def setUp(self):
        self.client = create_app(test=True).test_client()

    def tearDown(self):
        UserModel.drop_collection()

    @check_status_code(201)
    def test_signup_success(self):
        res = signup_request(self)
        self.assertTrue(UserModel.objects(name='test', device_uuid='test').first())
        return res

    @check_status_code(205)
    def test_exist_name(self):
        signup_request(self)
        return signup_request(self, device_uuid='sangmin')

    @check_status_code(205)
    def test_exist_deviceUUID(self):
        signup_request(self)
        return signup_request(self, name='sangmin')


class SigninTest(TestCase):

    def setUp(self):
        self.client = create_app(test=True).test_client()

    def tearDown(self):
        UserModel.drop_collection()

    @check_status_code(200)
    def test_success_signin(self):
        signup_request(self)
        return signin_reqeust(self)

    def test_fail_signin(self):
        return signin_reqeust(self)
