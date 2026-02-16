from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_admin import Admin, theme
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

loginManager = LoginManager()
loginManager.init_app(app)
loginManager.login_view = "login" # type: ignore

from app.models import User, Product, Brand, UserView, BrandView, ProductView
from app import routes

admin = Admin(app, name='Mueller Parts Index', theme=theme.BootstrapTheme(folder="bootstrap4",base_template="admin/base.html", swatch="slate",fluid=False))
admin.add_view(UserView(User, db.session))
admin.add_view(ProductView(Product, db.session))
admin.add_view(BrandView(Brand, db.session))
