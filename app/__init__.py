# from flask import Flask
# from config import Config
# from flask_sqlalchemy import SQLAlchemy
# from flask_security.datastore import SQLAlchemySessionUserDatastore
# from flask_security.core import Security

# # create flask app attribute of app package and set Config
# app = Flask(__name__)
# app.config.from_object(Config)

# # init database
# db = SQLAlchemy()
# db.init_app(app)

# #init Security
# from app.models import User, Role
# security = Security()
# user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)
# security.init_app(app, datastore=user_datastore)

# from app import routes
# from app.models import *

from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

loginManager = LoginManager()
loginManager.init_app(app)
loginManager.login_view = "login" # type: ignore

from app.models import User, Role  # import AFTER db is created
from app import routes 
