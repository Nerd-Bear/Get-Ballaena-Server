from . import parameter

CHECK_DEVICE_UUID_GET = {
    'tags': ['Account'],
    'description': '이미 가입 되어있는 device uuid인지 확인',
    'parameters': [
        parameter('deviceUUID', '디바이스 uuid', 'url')
    ],
    'responses': {
        '200': {
            'description': '가입된 device uuid'
        },
        '204': {
            'description': '가입 안되어 있는 device uuid'
        }
    }
}

AUTH_POST = {
    'tags': ['Account'],
    'description': '회원가입',
    'parameters': [
        parameter('name', '이름 or 닉네임'),
        parameter('deviceUUID', '디바이스 uuid', 'url')
    ],
    'responses': {
        '201': {
            'description': '인증 또는 회원가입 성공',
        },
        '205': {
            'description': '이미 존재하는 이름'
        }
    }
}
