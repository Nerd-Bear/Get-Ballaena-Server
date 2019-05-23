from unittest import TestCase
from unittest.mock import MagicMock, patch

from app import create_app
from tests.request import check_status_code, solve_get_request, solve_post_request


class SolveGetTest(TestCase):

    def setUp(self):
        self.client = create_app(test=True).test_client()

    @patch('view.solve.SolveView.check_time', MagicMock)
    @patch('model.BoothModel.get_booth_by_booth_name', return_value=MagicMock())
    @patch('view.solve.SolveView.is_booth_captured_by_user_team', return_value=False)
    @patch('view.solve.SolveView.is_in_delay', return_value=False)
    @patch('model.ProblemModel.get_random_problem', return_value=MagicMock(id='id',
                                                                           content='content',
                                                                           choices=['1', '2', '3', '4']))
    @check_status_code(200)
    def test_success(self,
                     get_random_problem_mock: MagicMock,
                     is_in_delay_mock: MagicMock,
                     is_booth_captured_by_user_team_mock: MagicMock,
                     get_both_by_booth_name: MagicMock):
        res = solve_get_request(self)

        get_both_by_booth_name.assert_called_once_with(booth_name='test')
        is_booth_captured_by_user_team_mock.assert_called_once_with(
            booth=get_both_by_booth_name.return_value
        )
        is_in_delay_mock.assert_called_once_with(
            booth=get_both_by_booth_name.return_value
        )
        get_random_problem_mock.assert_called_once_with()

        self.assertDictEqual({
            'boothName': 'test',
            'problemId': 'id',
            'content': 'content',
            'choices': ['1', '2', '3', '4']
        }, res.json)

        return res

    @patch('view.solve.SolveView.check_time', MagicMock)
    @patch('model.BoothModel.get_booth_by_booth_name', return_value=None)
    @patch('view.solve.SolveView.is_booth_captured_by_user_team', return_value=False)
    @patch('view.solve.SolveView.is_in_delay', return_value=False)
    @patch('model.ProblemModel.get_random_problem', return_value=MagicMock(id='id',
                                                                           content='content',
                                                                           choices=['1', '2', '3', '4']))
    @check_status_code(204)
    def test_wrong_booth_name(self,
                              get_random_problem_mock: MagicMock,
                              is_in_delay_mock: MagicMock,
                              is_booth_captured_by_user_team_mock: MagicMock,
                              get_both_by_booth_name: MagicMock):
        res = solve_get_request(self)

        get_both_by_booth_name.assert_called_once_with(booth_name='test')
        is_booth_captured_by_user_team_mock.assert_not_called()
        is_in_delay_mock.assert_not_called()
        get_random_problem_mock.assert_not_called()

        return res

    @patch('view.solve.SolveView.check_time', MagicMock)
    @patch('model.BoothModel.get_booth_by_booth_name', return_value=MagicMock())
    @patch('view.solve.SolveView.is_booth_captured_by_user_team', return_value=True)
    @patch('view.solve.SolveView.is_in_delay', return_value=False)
    @patch('model.ProblemModel.get_random_problem', return_value=MagicMock(id='id',
                                                                           content='content',
                                                                           choices=['1', '2', '3', '4']))
    @check_status_code(205)
    def test_already_captured_by_user_team(self,
                                           get_random_problem_mock: MagicMock,
                                           is_in_delay_mock: MagicMock,
                                           is_booth_captured_by_user_team_mock: MagicMock,
                                           get_both_by_booth_name: MagicMock):
        res = solve_get_request(self)

        get_both_by_booth_name.assert_called_once_with(booth_name='test')
        is_booth_captured_by_user_team_mock.assert_called_once_with(booth=get_both_by_booth_name.return_value)
        is_in_delay_mock.assert_not_called()
        get_random_problem_mock.assert_not_called()

        return res

    @patch('view.solve.SolveView.check_time', MagicMock)
    @patch('model.BoothModel.get_booth_by_booth_name', return_value=MagicMock())
    @patch('view.solve.SolveView.is_booth_captured_by_user_team', return_value=False)
    @patch('view.solve.SolveView.is_in_delay', return_value=True)
    @patch('view.solve.SolveView.get_left_delay', return_value='30:00')
    @patch('model.ProblemModel.get_random_problem', return_value=MagicMock(id='id',
                                                                           content='content',
                                                                           choices=['1', '2', '3', '4']))
    @check_status_code(409)
    def test_in_delay(self,
                      get_random_problem_mock: MagicMock,
                      get_left_delay_mock: MagicMock,
                      is_in_delay_mock: MagicMock,
                      is_booth_captured_by_user_team_mock: MagicMock,
                      get_both_by_booth_name: MagicMock):
        res = solve_get_request(self)

        get_both_by_booth_name.assert_called_once_with(booth_name='test')
        is_booth_captured_by_user_team_mock.assert_called_once_with(booth=get_both_by_booth_name.return_value)
        is_in_delay_mock.assert_called_once_with(booth=get_both_by_booth_name.return_value)
        get_left_delay_mock.assert_called_once_with(booth=get_both_by_booth_name.return_value)
        get_random_problem_mock.assert_not_called()

        self.assertDictEqual({
            'delayTime': '30:00'
        }, res.json)

        return res


class SolvePostTest(TestCase):

    def setUp(self):
        self.client = create_app(test=True).test_client()

    @patch('model.ProblemModel.get_problem_by_id', return_value=MagicMock(answer='test'))
    @patch('model.BoothModel.get_booth_by_booth_name', return_value=MagicMock())
    @patch('view.solve.SolveView.is_in_delay', return_value=False)
    @patch('view.solve.SolveView.get_current_user', return_value=MagicMock())
    @check_status_code(201)
    def test_success(self,
                     get_current_user_mock: MagicMock,
                     is_in_delay_mock: MagicMock,
                     get_booth_by_booth_name_mock: MagicMock,
                     get_problem_by_id_mock: MagicMock):
        res = solve_post_request(self)

        booth = get_booth_by_booth_name_mock.return_value
        get_problem_by_id_mock.assert_called_once_with(id='test')
        get_booth_by_booth_name_mock.assert_called_once_with(booth_name='test')
        is_in_delay_mock.assert_called_once_with(
            booth=booth
        )
        get_current_user_mock.assert_called_once_with()
        booth.capture.assert_called_once_with(
            user=get_current_user_mock.return_value
        )

        return res

    @patch('model.ProblemModel.get_problem_by_id', return_value=None)
    @patch('model.BoothModel.get_booth_by_booth_name', return_value=MagicMock())
    @patch('view.solve.SolveView.is_in_delay', return_value=False)
    @patch('view.solve.SolveView.get_current_user', return_value=MagicMock())
    @check_status_code(204)
    def test_wrong_problem_id(self,
                              get_current_user_mock: MagicMock,
                              is_in_delay_mock: MagicMock,
                              get_booth_by_booth_name_mock: MagicMock,
                              get_problem_by_id_mock: MagicMock):
        res = solve_post_request(self)

        booth = get_booth_by_booth_name_mock.return_value
        get_problem_by_id_mock.assert_called_once_with(id='test')
        get_booth_by_booth_name_mock.assert_called_once_with(booth_name='test')
        is_in_delay_mock.assert_not_called()
        get_current_user_mock.assert_not_called()
        booth.capture.assert_not_called()

        return res

    @patch('model.ProblemModel.get_problem_by_id', return_value=MagicMock())
    @patch('model.BoothModel.get_booth_by_booth_name', return_value=None)
    @patch('view.solve.SolveView.is_in_delay', return_value=False)
    @patch('view.solve.SolveView.get_current_user', return_value=MagicMock())
    @check_status_code(204)
    def test_wrong_booth_name(self,
                              get_current_user_mock: MagicMock,
                              is_in_delay_mock: MagicMock,
                              get_booth_by_booth_name_mock: MagicMock,
                              get_problem_by_id_mock: MagicMock):
        res = solve_post_request(self)

        get_problem_by_id_mock.assert_called_once_with(id='test')
        get_booth_by_booth_name_mock.assert_called_once_with(booth_name='test')
        is_in_delay_mock.assert_not_called()
        get_current_user_mock.assert_not_called()

        return res

    @patch('model.ProblemModel.get_problem_by_id', return_value=MagicMock(answer='wrong'))
    @patch('model.BoothModel.get_booth_by_booth_name', return_value=MagicMock())
    @patch('view.solve.SolveView.is_in_delay', return_value=False)
    @patch('view.solve.SolveView.get_current_user', return_value=MagicMock())
    @check_status_code(205)
    def test_wrong_answer(self,
                          get_current_user_mock: MagicMock,
                          is_in_delay_mock: MagicMock,
                          get_booth_by_booth_name_mock: MagicMock,
                          get_problem_by_id_mock: MagicMock):
        res = solve_post_request(self)

        booth = get_booth_by_booth_name_mock.return_value
        get_problem_by_id_mock.assert_called_once_with(id='test')
        get_booth_by_booth_name_mock.assert_called_once_with(booth_name='test')
        is_in_delay_mock.assert_called_once_with(
            booth=booth
        )
        booth.set_delay.assert_called_once_with(minutes=1)
        get_current_user_mock.assert_not_called()
        booth.capture.assert_not_called()

        return res

    @patch('model.ProblemModel.get_problem_by_id', return_value=MagicMock(answer='test'))
    @patch('model.BoothModel.get_booth_by_booth_name', return_value=MagicMock())
    @patch('view.solve.SolveView.is_in_delay', return_value=True)
    @patch('view.solve.SolveView.get_left_delay', return_value='30:00')
    @patch('view.solve.SolveView.get_current_user', return_value=MagicMock())
    @check_status_code(409)
    def test_in_delay(self,
                      get_current_user_mock: MagicMock,
                      get_left_delay_mock: MagicMock,
                      is_in_delay_mock: MagicMock,
                      get_booth_by_booth_name_mock: MagicMock,
                      get_problem_by_id_mock: MagicMock):
        res = solve_post_request(self)

        booth = get_booth_by_booth_name_mock.return_value

        get_problem_by_id_mock.assert_called_once_with(id='test')
        get_booth_by_booth_name_mock.assert_called_once_with(booth_name='test')
        is_in_delay_mock.assert_called_once_with(booth=booth)
        get_left_delay_mock.assert_called_once_with(booth=booth)
        get_current_user_mock.assert_not_called()
        booth.capture.assert_not_called()

        self.assertDictEqual({
            'delayTime': '30:00'
        }, res.json)

        return res
