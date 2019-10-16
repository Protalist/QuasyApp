from flask import render_template

from app import app
from app.models import Song

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"

@app.route('/song')
def songs():
    songs=Song.query.all()
    return render_template('songs.html', songs=songs)