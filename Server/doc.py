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
        parameter('deviceUUID', '디바이스 uuid', 'url'),
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
                        '고래 유적지': {
                            'team': 1,
                            'latitude': 12.424121,
                            'longitude': 52.321121,
                        },
                        '고래 광장': {
                            'team': 0,
                            'latitude': 44.32532,
                            'longitude': 33.42432,
                        },
                        '관리 사무소': {
                            'team': -1,
                            'latitude': 34.32532,
                            'longitude': 55.42432,
                        },
                    },
                    'myTeam': '흰수염고래',
                }
            }
        }
    }
}

WEB_MAP_GET = {
    'tags': ['Map'],
    'description': '웹 현재 맵 상황',
    'parameters': [],
    'responses': {
        '200': {
            'description': """get 성공
            빈 스트링: 점령되지 않음
            """,
            'examples': {
                '': {
                    'map': {
                        '고래 유적지': {
                            'teamName': '범고래팀',
                            'latitude': 12.424121,
                            'longitude': 52.321121,
                        },
                        '고래 광장': {
                            'teamName': '돌고래팀',
                            'latitude': 44.32532,
                            'longitude': 33.42432,
                        },
                        '관리 사무소': {
                            'teamName': '',
                            'latitude': 34.32532,
                            'longitude': 55.42432,
                        },
                    },
                }
            }
        }
    }
}

ALWAYS_MAP_GET = {
    'tags': ['Map'],
    'description': '상시 맵',
    'parameters': [device_uuid],
    'responses': {
        '200': {
            'description': """get 성공
            true: 캡쳐됨
            false: 캡쳐 안됨
            """,
            'examples': {
                '': {
                    'map': {
                        '고래 유적지': {
                            'captured': True,
                            'latitude': 12.424121,
                            'longitude': 52.321121,
                        },
                        '고래 광장': {
                            'captured': False,
                            'latitude': 44.32532,
                            'longitude': 33.42432,
                        },
                        '관리 사무소': {
                            'captured': False,
                            'latitude': 34.32532,
                            'longitude': 55.42432,
                        },
                    },
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
                    '범고래팀': {
                        'member': [
                            'ㅁㅁ',
                            'ㅇㅇ',
                            'ㄷㄷ'
                        ],
                    },
                    '흰수염고래팀': {
                        'member': [
                            'aa',
                            'dd'
                        ]
                    },
                    '돌고래팀': {
                        'member': []
                    },
                    '일각고래팀': {
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
        parameter('teamName', '팀 이름')
    ],
    'responses': {
        '201': {
            'description': '참가 성공'
        },
        '204': {
            'description': '이미 팀에 소속되어 있음'
        },
        '205': {
            'description': '잘못된 팀 이름'
        },
    }
}
