from functools import wraps


def check_status_code(status_code):
    def decorator(fn):
        @wraps(fn)
        def wrapper(self, *args, **kwargs):
            rv = fn(self, *args, **kwargs)
            self.assertEqual(status_code, rv.status_code)

        return wrapper

    return decorator


def signup_request(self, *, device_uuid: str='test', name: str='test'):
    return self.client.post(
        f'/auth/{device_uuid}',
        json={'name': name}
    )


def signin_reqeust(self, *, device_uuid: str='test', name: str='test'):
    return self.client.get(
        f'/auth/{device_uuid}'
    )
