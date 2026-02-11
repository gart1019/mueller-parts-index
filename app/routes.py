from flask import render_template, url_for, redirect, request
from app import app, db
from app.forms import LoginForm
from app.models import User, Role
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from sqlalchemy import select
from urllib.parse import urlsplit


@app.route('/')
@app.route('/dashboard')
@login_required
def dashboard():
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
# @login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/register')
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('register.html')

@app.route('/inventory')
@login_required
def inventory():
    return render_template('inventory.html')

@app.route('/lookup')
def lookup():
    return render_template('lookup.html')