from test import TCBase, check_status_code
from test.requests import check_device_uuid_request


class CheckGameKeyTest(TCBase):

    @check_status_code(200)
    def test_success_check_game_key(self):
        return check_device_uuid_request(self)

    @check_status_code(204)
    def test_wrong_game_key(self):
        return check_device_uuid_request(self, 111111)
