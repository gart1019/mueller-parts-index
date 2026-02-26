import os

from dotenv import find_dotenv, load_dotenv

path = find_dotenv()
load_dotenv(path, override=True)

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'asdfgshyjjnbvxcr'

    SQLALCHEMY_ENGINES = {"default": "sqlite:///db.sqlite"}
    SQLALCHEMY_DATABASE_URI = "sqlite:///db.sqlite"
    
    RECAPTCHA_PUBLIC_KEY = "6Lf-UmQsAAAAAKbEmMDYdT2FPwHwA-3E8kiLvzp5"
    RECAPTCHA_PRIVATE_KEY = os.environ.get('CAPTCHA_KEY')
    RECAPTCHA_DATA_ATTRS = {'theme': 'dark'}

    MAIL_SERVER = os.environ.get("MAIL_SERVER")
    MAIL_PORT = int(os.environ.get("MAIL_PORT", 587))
    MAIL_USE_TLS = True  # Use TLS for most SMTP providers
    MAIL_USE_SSL = False  # Use SSL only if required (never enable both)
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = ("Mueller Index", "no-reply@notifications.muellerindex.org")
    MAIL_DEBUG = True
    MAIL_TIMEOUT = 10
    TESTING = False