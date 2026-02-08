import os

from dotenv import find_dotenv, load_dotenv

path = find_dotenv()
load_dotenv(path)

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'bad key'
    SQLALCHEMY_ENGINES = {"default": "sqlite:///default.sqlite"}
    SECURITY_PASSWORD_SALT = os.environ.get('SALT')
    REMEMBER_COOKIE_SAMESITE = 'strict'
    SESSION_COOKIE_SAMESITE = 'strict'
    SQLALCHEMY_ENGINES = {'default': "sqlite:///db.sqlite3"}

    