from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Email, Length
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User

class LoginForm(FlaskForm):
    username = StringField("Email", validators=[DataRequired(message="An email is required")])
    password = PasswordField("Password", validators=[DataRequired(message="A password is required")])
    remember_me = BooleanField("Remember Me")
    # recaptcha = RecaptchaField()
    submit = SubmitField("Sign In")

    def validate_username(self, username):
        user = User.query.filter_by(email=username.data).first()
        if user is None or not user.check_password(self.password.data):
            raise ValidationError(message="Invalid username or password")   

class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(message="An email is required"), Email(message="A valid email is required"), Length(max=50)])
    full_name = StringField("Full Name", validators=[DataRequired(message="Your first & last name are required"), Length(max=25)])
    password = PasswordField("Password", validators=[DataRequired(message="A password is required"), Length(min=8,max=20,message="Your password must be between 8 & 20 characters long")])
    # recaptcha = RecaptchaField()
    submit = SubmitField("Register")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError(message="This email is already in use")