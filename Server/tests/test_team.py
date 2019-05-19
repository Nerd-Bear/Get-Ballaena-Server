from unittest import TestCase
from unittest.mock import MagicMock, patch

from tests.request import check_status_code, signup_request, team_list_request, team_join_request
from app import create_app
from model import UserModel, TeamModel


def create_team_list_mock():
    team_list = []
    for i in range(5):
        team = MagicMock()
        team.team_name = f'team {i}'
        team_list.append(team)
    return team_list


def create_user_list_mock():
    user_list = []
    for i in range(5):
        user = MagicMock()
        user.name = f'user {i}'
        user_list.append(user)
    return user_list


class TeamListTest(TestCase):

    def setUp(self):
        self.client = create_app(test=True).test_client()
        signup_request(self)

    def tearDown(self):
        UserModel.drop_collection()

    @patch('model.TeamModel.objects', return_value=create_team_list_mock())
    @patch('model.UserModel.objects', return_value=create_user_list_mock())
    @check_status_code(200)
    def test_success(self, user_mock, team_mock):
        return team_list_request(self)


class TeamJoinTest(TestCase):

    def setUp(self):
        self.client = create_app(test=True).test_client()
        signup_request(self)

    def tearDown(self):
        UserModel.drop_collection()

    @patch('view.team.TeamView.get_current_user', return_value=MagicMock(team=None))
    @patch('view.team.TeamView.get_team', return_value=MagicMock())
    @check_status_code(201)
    def test_success(self, team_mock, user_mock):
        res = team_join_request(self)
        self.assertEqual(user_mock.return_value.team, team_mock.return_value)
        return res

    @patch('view.team.TeamView.get_current_user', return_value=MagicMock(team='team'))
    @patch('view.team.TeamView.get_team', return_value=MagicMock())
    @check_status_code(204)
    def test_already_joined_team(self, team_mock, user_mock):
        res = team_join_request(self)
        self.assertEqual(user_mock.return_value.team, 'team')
        return res

    @patch('view.team.TeamView.get_current_user', return_value=MagicMock(team=None))
    @patch('view.team.TeamView.get_team', return_value=None)
    @check_status_code(205)
    def test_wrong_team(self, team_mock, user_mock):
        res = team_join_request(self)
        self.assertEqual(user_mock.return_value.team, None)
        return res
