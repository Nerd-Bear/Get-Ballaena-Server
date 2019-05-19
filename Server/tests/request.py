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


def signup_request(self, *, device_uuid: str='test', name: str='test') -> Response:
    return self.client.post(
        f'/auth/{device_uuid}',
        json={'name': name},
    )


def signin_request(self, *, device_uuid: str='test') -> Response:
    return self.client.get(
        f'/auth/{device_uuid}',
    )


def stamp_map_request(self, *, device_uuid: str='test') -> Response:
    return self.client.get(
        f'/stamp/map',
        headers={'deviceUUID': device_uuid},
    )


def stamp_capture_request(self, *, device_uuid: str='test', stamp_name: str='stamp 0') -> Response:
    return self.client.post(
        f'/stamp',
        headers={'deviceUUID': device_uuid},
        json={'stampName': stamp_name},
    )
