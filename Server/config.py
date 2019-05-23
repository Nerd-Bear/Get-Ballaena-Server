import os
from datetime import datetime


class Config:
    JSON_AS_ASCII = False

    JWT_SECRET_KEY = os.getenv('SECRET_KEY', 'nerd-bear')
    SECRET_KEY = os.getenv('SECRET_KEY', 'nerd-bear')

    START_TIME = datetime(2020, 4, 20, 12, 00)
    END_TIME = datetime(2020, 4, 20, 12, 30)
