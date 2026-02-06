import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'bad key'
    SQLALCHEMY_ENGINES = {"default": "sqlite:///default.sqlite"}