from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from werkzeug.security import generate_password_hash
from app.models import User

class LoginForm(FlaskForm):
    username = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    # recaptcha = RecaptchaField()
    submit = SubmitField("Sign In")

    def validate_username(self, username):
        user = User.query.filter_by(email=username.data).first()
        if user is None:
            raise ValidationError()
        
    # def validate_password(self, password):
    #     user = User.query.filter_by(password_hash=generate_password_hash(password.data)).first()
    #     if user is None:
    #         raise ValidationError('Incorrect email or password.')
