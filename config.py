import os

from dotenv import find_dotenv, load_dotenv

path = find_dotenv()
load_dotenv(path)

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'bad key'

    SQLALCHEMY_ENGINES = {"default": "sqlite:///db.sqlite"}
    SQLALCHEMY_DATABASE_URI = "sqlite:///db.sqlite"
    
    RECAPTCHA_PUBLIC_KEY = "6Lf-UmQsAAAAAKbEmMDYdT2FPwHwA-3E8kiLvzp5"
    RECAPTCHA_PRIVATE_KEY = os.environ.get('CAPTCHA_KEY')
    RECAPTCHA_DATA_ATTRS = {'theme': 'dark'}
    