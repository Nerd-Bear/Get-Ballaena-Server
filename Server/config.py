import os


class Config:
    SERVICE_NAME = 'Get Terra'

    SWAGGER = {
        'title': SERVICE_NAME,
        'specs_route': os.getenv('SWAGGER_URI', '/docs'),
        'uiversion': 3,

        'info': {
            'title': SERVICE_NAME + ' API',
            'version': '1.0',
            'description': ''
        },
        'host': 'ec2.istruly.sexy',
        'basePath': '/',
    }

    SWAGGER_TEMPLATE = {
        'schemes': [
            'http'
        ],
        'tags': [
            {
                'name': 'Account',
                'description': '계정 관련 API'
            },
            {
                'name': 'Map',
                'description': '맵 관련 API'
            },
            {
                'name': 'Solve',
                'description': '문제 풀이 관련 API'
            },
            {
                'name': 'Team',
                'description': '팀 관련 API'
            }
        ]
    }
