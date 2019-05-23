from functools import wraps
from flask import Response


def check_status_code(status_code):
    def decorator(fn):
        @wraps(fn)
        def wrapper(self, *args, **kwargs):
            rv = fn(self, *args, **kwargs)
            self.assertEqual(status_code, rv.status_code)

        return wrapper

    return decorator


def signup_request(self, *,
                   device_uuid: str='test',
                   name: str='test') -> Response:
    return self.client.post(
        f'/auth/{device_uuid}',
        json={'name': name},
    )


def signin_request(self, *,
                   device_uuid: str='test') -> Response:
    return self.client.get(
        f'/auth/{device_uuid}',
    )


def stamp_map_request(self, *,
                      device_uuid: str='test') -> Response:
    return self.client.get(
        '/stamp/map',
        headers={'deviceUUID': device_uuid},
    )


def stamp_capture_request(self, *,
                          device_uuid: str='test',
                          stamp_name: str='stamp 0') -> Response:
    return self.client.post(
        '/stamp',
        headers={'deviceUUID': device_uuid},
        json={'stampName': stamp_name},
    )


def team_list_request(self, *,
                      device_uuid: str='test') -> Response:
    return self.client.get(
        '/team',
        headers={'deviceUUID': device_uuid}
    )


def team_join_request(self, *,
                      device_uuid: str='test',
                      join_code='join') -> Response:
    return self.client.post(
        '/team',
        headers={'deviceUUID': device_uuid},
        json={'joinCode': join_code},
    )


def coupon_list_request(self, *,
                        device_uuid: str='test') -> Response:
    return self.client.get(
        '/coupon',
        headers={'deviceUUID': device_uuid},
    )


def coupon_delete_request(self, *,
                          device_uuid: str='test',
                          coupon_id: str='5ce23b5083b01a99ce56c996',
                          staff_code: str='20190607') -> Response:
    return self.client.delete(
        f'/coupon?coupon_id={coupon_id}',
        headers={'deviceUUID': device_uuid},
        json={'staffCode': staff_code},
    )


def map_request(self, *, device_uuid: str='test'):
    return self.client.get(
        '/map',
        headers={'deviceUUID': device_uuid},
    )


def solve_get_request(self, *,
                      device_uuid: str='test',
                      booth_name: str='test'):
    return self.client.get(
        f'/solve/{booth_name}',
        headers={'deviceUUID': device_uuid},
    )


def solve_post_request(self, *,
                       device_uuid: str='test',
                       booth_name: str='test',
                       problem_id: str='test',
                       answer: str='test'):
    return self.client.post(
        f'/solve/{booth_name}',
        headers={'deviceUUID': device_uuid},
        json={'problemId': problem_id, 'answer': answer},
    )
