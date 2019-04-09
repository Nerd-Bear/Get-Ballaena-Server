from json import dumps


def check_game_key_request(self, device_uuid='test_uuid'):
    return self.client.get(
        f'/auth/{device_uuid}'
    )


def auth_post_request(self, device_uuid='test_uuid', name='sangmin'):
    return self.client.post(
        f'/auth/{device_uuid}',
        data=dumps({'name': name}),
        content_type='application/json'
    )


def map_get_request(self, device_uuid='test_uuid'):
    return self.client.get(
        '/map',
        headers={'deviceUUID': device_uuid}
    )


def solve_get_request(self, booth_name='test_booth', device_uuid='test_uuid'):
    return self.client.get(
        f'/solve/{booth_name}',
        headers={'deviceUUID': device_uuid}
    )


def solve_post_request(self, problem_id: str, booth_name='test_booth', answer='1', device_uuid='test_uuid'):
    return self.client.post(
        f'/solve/{booth_name}',
        data=dumps(dict(problemId=problem_id, answer=answer)),
        content_type='application/json',
        headers={'deviceUUID': device_uuid}
    )


def team_get_request(self, device_uuid='test_uuid'):
    return self.client.get(
        '/team',
        headers={'deviceUUID': device_uuid}
    )


def team_post_request(self, team_name='test_team', device_uuid='test_uuid'):
    return self.client.post(
        '/team',
        data=dumps({'teamName': team_name}),
        content_type='application/json',
        headers={'deviceUUID': device_uuid}
    )
