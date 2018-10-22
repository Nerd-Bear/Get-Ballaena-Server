from . import parameter, jwt_header

TEAM_GET = {
    'tags': ['Team'],
    'description': '팀별 팀원 리스트',
    'parameters': [
        jwt_header
    ],
    'responses': {
        '200': {
            'description': 'get 성공',
            'examples': {
                '': {
                    'blue': [
                        'ㅁㅁ',
                        'ㅇㅇ',
                        'ㄷㄷ'
                    ],
                    'green': [
                        'aa',
                        'dd'
                    ],
                    'yellow': [],
                    'violet': [
                        '상미니'
                    ]
                }
            }
        },
        '401': {
            'description': 'request header 에 access token 없음 '
        },
        '403': {
            'description': '권한 없음'
        }
    }
}

TEAM_POST = {
    'tags': ['Team'],
    'description': '팀 참가',
    'parameters': [
        jwt_header,
        parameter('team', '''팀 종류 empty, blue, green, yellow, violet''', 'query string')
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
        },
        '401': {
            'description': 'request header 에 access token 없음 '
        },
        '403': {
            'description': '권한 없음'
        }
    }
}