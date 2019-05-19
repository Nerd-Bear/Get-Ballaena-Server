import os


class Config:
    JSON_AS_ASCII = False

    JWT_SECRET_KEY = os.getenv('SECRET_KEY', 'nerd-bear')
    SECRET_KEY = os.getenv('SECRET_KEY', 'nerd-bear')
