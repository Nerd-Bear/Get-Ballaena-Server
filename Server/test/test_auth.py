from unittest import TestCase
from unittest.mock import patch, MagicMock

from test.requests import check_device_uuid_request

from app import create_app


def make_first_mock(return_value):
    mock_objects = MagicMock()
    mock_objects.first = MagicMock()
    mock_objects.first.return_value = return_value
    return mock_objects


class TestAuth(TestCase):

    def setUp(self):
        self.client = create_app().test_client()

    @patch('model.UserModel.objects', return_value=make_first_mock(None))
    def test_get_success(self, mock_user_model: MagicMock):
        res = check_device_uuid_request(self)
        self.assertEqual(res.status_code, 200)

    @patch('model.UserModel.objects', return_value=make_first_mock(MagicMock()))
    def test_get_failed(self, mock_user_model: MagicMock):
        res = check_device_uuid_request(self)
        self.assertEqual(res.status_code, 204)
