from flask import render_template, url_for, redirect, request
from app import app, db, mail
from app.forms import LoginForm, RegisterForm
from app.models import User, Role
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from app.email_utils import generate_token, confirm_token, send_verification_email
from sqlalchemy import select
from urllib.parse import urlsplit


@app.route('/')
@app.route('/dashboard')
@login_required
def dashboard():
    print("running")
    if not current_user.account_active or not current_user.email_verified:
        return redirect(url_for('inactive'))
    return render_template('dashboard.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.username.data).first()

        if user is None or not user.check_password(form.password.data): #fail block
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data) #success

        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '': #where to go next
            next_page = url_for('dashboard')
       
        return redirect(next_page)
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated: #technically dont need both
        return redirect(url_for('dashboard'))
    
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(e=form.email.data, n=form.full_name.data)
        user.set_password(password=form.password.data)
        db.session.add(user)
        db.session.commit()
        db.session.refresh(user)

        token = generate_token(form.email.data) #sign a token representing the users email
        verification_url = url_for('verify', token=token, _external=True) #external to create absolute url
        send_verification_email(form.email.data, form.full_name.data, verification_url=verification_url) #send email with link

        print("db flag:", user.__dict__.get("active") or user.__dict__.get("is_active"))
        print("flask-login is_active:", current_user.is_active)

        return render_template('register.html', form=form, email_feedback="Please check your inbox!")
    return render_template('register.html', form=form, email_feedback=None)



@app.route('/verify/<token>')
def verify(token):
    email = confirm_token(token)
    user = User.query.filter_by(email=email).first()

    if email and user is not None:
        user.email_verified = True
        db.session.add(user)
        db.session.commit()
        db.session.refresh(user)
        return "You have been verified, you may now log in!<br>Please ensure your network admin has accepted your registration for site-wide access."
    else:
        return redirect(url_for('error'))

@app.route('/error')
def error():
    return render_template('error.html')

@app.route('/inactive')
def inactive():
    if current_user is not None:
        logout()
    return render_template('inactive.html')

