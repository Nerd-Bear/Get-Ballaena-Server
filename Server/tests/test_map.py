from unittest import TestCase
from unittest.mock import MagicMock, patch

from app import create_app
from tests.request import map_request, check_status_code


def create_booth_mock_list():
    return [MagicMock(booth_name=f'booth {i}', own_team=MagicMock(team_name=f'team {i}'), x=i, y=i) for i in range(10)]


class MapTest(TestCase):

    def setUp(self):
        self.client = create_app(test=True).test_client()

    @patch('view.map.MapView.check_time', MagicMock)
    @patch('view.map.MapView.get_team_name', return_value='team 0')
    @patch('view.map.MapView.get_left_time', return_value='30:00')
    @patch('model.BoothModel.get_all_booths', return_value=create_booth_mock_list())
    @check_status_code(200)
    def test_success(self,
                     get_all_booths_mock: MagicMock,
                     get_left_time_mock: MagicMock,
                     get_team_name_mock: MagicMock):
        res = map_request(self)

        get_team_name_mock.assert_called_once_with()
        get_left_time_mock.assert_called_once_with()
        get_all_booths_mock.assert_called_once_with()

        self.assertDictEqual({
            'map': [dict(booth_name=f'booth {i}', own_team=f'team {i}', x=i, y=i) for i in range(10)],
            'myTeam': 'team 0',
            'leftTime': '30:00'
        }, res.json)

        return res
