from flask import render_template, url_for, redirect, request
from app import app, db
from app.forms import LoginForm, RegisterForm
from app.models import User, Role
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from sqlalchemy import select
from urllib.parse import urlsplit


@app.route('/')
@app.route('/dashboard')
@login_required
def dashboard():
    if not current_user.account_active:
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
    if current_user.is_authenticated and current_user.account_active:
        return redirect(url_for('dashboard'))
    
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(e=form.email.data, n=form.full_name.data)
        user.set_password(password=form.password.data)
        db.session.add(user)
        db.session.commit()
        db.session.refresh(user)

        login_user(user=user)
        print("db flag:", user.__dict__.get("active") or user.__dict__.get("is_active"))
        print("flask-login is_active:", current_user.is_active)

        return redirect(url_for('inactive'))

    return render_template('register.html', form=form)




@app.route('/inactive')
@login_required
def inactive():
    if current_user.account_active:
        return redirect(url_for('dashboard'))
    return render_template('inactive.html')

@app.route('/verify/<id>')
@login_required
def inventory(id):
    user = User.query.filter_by()

    return render_template('inventory.html')

# @app.route('/dashboard/inventory/configure')
# @login_required
# def config_inventory():
#     return render_template('base.html')

# @app.route('/dashboard/team')
# @login_required
# def team():
#     members = User.query.all()
#     return render_template('team_page.html', members=members)