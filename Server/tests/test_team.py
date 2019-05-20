from unittest import TestCase
from unittest.mock import MagicMock, patch, call

from app import create_app
from tests.request import check_status_code, team_list_request, team_join_request


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

    @patch('model.TeamModel.get_all_teams', return_value=create_team_list_mock())
    @patch('model.UserModel.get_users_by_team', return_value=create_user_list_mock())
    @check_status_code(200)
    def test_success(self,
                     get_users_by_team_mock: MagicMock,
                     get_all_teams_mock: MagicMock):
        res = team_list_request(self)

        get_all_teams_mock.assert_called_once()
        get_users_by_team_mock.assert_has_calls(
            [call(team) for team in get_all_teams_mock.return_value],
            any_order=True
        )
        return res


class TeamJoinTest(TestCase):

    def setUp(self):
        self.client = create_app(test=True).test_client()

    @patch('view.team.TeamView.get_current_user', return_value=MagicMock(team=None))
    @patch('model.TeamModel.get_team_by_team_name', return_value=MagicMock())
    @check_status_code(201)
    def test_success(self,
                     get_team_by_team_name_mock: MagicMock,
                     get_current_user_mock: MagicMock):
        res = team_join_request(self)

        get_current_user_mock.assert_called_once()
        get_team_by_team_name_mock.assert_called_with(team_name='team 0')

        self.assertEqual(
            get_current_user_mock.return_value.team,
            get_team_by_team_name_mock.return_value
        )

        return res

    @patch('view.team.TeamView.get_current_user', return_value=MagicMock(team='team'))
    @patch('model.TeamModel.get_team_by_team_name', return_value=MagicMock())
    @check_status_code(204)
    def test_already_joined_team(self,
                                 get_team_by_team_name_mock: MagicMock,
                                 get_current_user_mock: MagicMock):
        res = team_join_request(self)

        get_current_user_mock.assert_called_once()
        get_team_by_team_name_mock.assert_not_called()

        self.assertEqual(get_current_user_mock.return_value.team, 'team')
        return res

    @patch('view.team.TeamView.get_current_user', return_value=MagicMock(team=None))
    @patch('model.TeamModel.get_team_by_team_name', return_value=None)
    @check_status_code(205)
    def test_wrong_team(self,
                        get_team_by_team_name_mock: MagicMock,
                        get_current_user_mock: MagicMock):
        res = team_join_request(self)

        get_current_user_mock.assert_called_once()
        get_team_by_team_name_mock.assert_called_with(team_name='team 0')

        self.assertEqual(get_current_user_mock.return_value.team, None)
        return res
