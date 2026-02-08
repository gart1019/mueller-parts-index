from flask import Flask
from config import Config
from flask_sqlalchemy_lite import SQLAlchemy

# create flask app attribute of app package and set Config
app = Flask(__name__)
app.config.from_object(Config)

# init database
db = SQLAlchemy()
db.__init__(app=app)

from app import routes
from app.models import *

