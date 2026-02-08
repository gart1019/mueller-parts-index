from flask import render_template, url_for
from app import app
from app.forms import LoginForm


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        return render_template('lookup.html', form=form)

    return render_template('login.html', form=form)

@app.route('/lookup')
def lookup():
    return render_template('lookup.html')