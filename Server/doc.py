def parameter(name, description, in_='json', type='str', required=True):
    return {
        'name': name,
        'description': description,
        'in': in_,
        'type': type,
        'required': required
    }


device_uuid = parameter('deviceUUID', 'device uuid', 'header')
game_key = parameter('gameKey', '게임 인증키', 'uri', 'int')

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

SOLVE_GET = {
    'tags': ['Solve'],
    'description': '문제 get',
    'parameters': [
        device_uuid,
        parameter('boothName', '부스 이름', 'url')
    ],
    'responses': {
        '200': {
            'description': '성공',
            'examples': {
                '': {
                    'boothName': '부스 이름',
                    'problemId': '문제 아이디',
                    'content': '문제 내용',
                    'choices': [
                        '1번 보기',
                        '2번 보기',
                        '3번 보기',
                        '4번 보기'
                    ]
                }
            }
        },
        '204': {
            'description': '해당 부스아이디에 해당하는 부스 없음'
        },
        '205': {
            'description': '이미 해당팀에서 점령한 부스임'
        },
        '408': {
            'description': '딜레이 시간'
        }
    }
}

SOLVE_POST = {
    'tags': ['Solve'],
    'description': '문제 정답 제출',
    'parameters': [
        device_uuid,
        parameter('boothName', '부스 이름', 'url'),
        parameter('problemId', '문제 아이디'),
        parameter('answer', '정답 (보기 내용 ex. 1번 보기)')
    ],
    'responses': {
        '201': {
            'description': '정답'
        },
        '204': {
            'description:': '잘못된 문제 아이디 또는 잘못된 동아리 아이디'
        },
        '205': {
            'description': '오답'
        },
        '408': {
            'description': '딜레이 시간'
        }
    }
}

MAP_GET = {
    'tags': ['Map'],
    'description': '안드로이드 현재 맵 상황',
    'parameters': [device_uuid],
    'responses': {
        '200': {
            'description': """get 성공
            1: 우리팀이 점령함
            0: 다른팀이 점령함
            -1: 아직 점령이 안됨
            """,
            'examples': {
                '': {
                    'map': {
                        'GRAM': 1,
                        '시나브로': 0,
                        'Undefined': 1,
                        'NoNamed': -1,
                        'LUNA': -1
                    },
                    'myTeam': '흰수염고래',
                }
            }
        }
    }
}

TEAM_GET = {
    'tags': ['Team'],
    'description': '팀별 팀원 리스트',
    'parameters': [
        device_uuid
    ],
    'responses': {
        '200': {
            'description': 'get 성공',
            'examples': {
                '': {
                    '흰수염고래': {
                        'member': [
                            'ㅁㅁ',
                            'ㅇㅇ',
                            'ㄷㄷ'
                        ],
                    },
                    '돌고래': {
                        'member': [
                            'aa',
                            'dd'
                        ]
                    },
                    '술고래': {
                        'member': []
                    },
                    '고래고래': {
                        'member': ['상민이']
                    }
                }
            }
        }
    }
}

TEAM_POST = {
    'tags': ['Team'],
    'description': '팀 참가',
    'parameters': [
        device_uuid,
        parameter('teamName', '팀 이름', 'json')
    ],
    'responses': {
        '201': {
            'description': '참가 성공'
        },
        '204': {
            'description': '이미 팀에 소속되어 있음'
        },
        '205': {
            'description': '팀원 초과, 잘못된 팀 번호'
        }
    }
}
