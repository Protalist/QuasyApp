from flask import render_template, flash, redirect

from app import app
from app.models import Song
from app.forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"

@app.route('/song')
def songs():
    songs=Song.query.all()
    return render_template('songs.html', songs=songs)

@app.route('/login')
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect('/index')
    return render_template('login.html', title='Sign In', form=form)