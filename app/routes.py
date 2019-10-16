import flask
from flask import render_template, flash, redirect

from app import app, db
from app.models import Song
from app.forms import LoginForm
from flask import render_template
from flask import url_for
from flask import request,jsonify
from flask import render_template, flash
from flask import redirect
from flask import session


@app.route('/')
@app.route('/index')
def index():
    return render_template("base.html")

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



@app.route("/searchs",methods=["GET"])
def searchsong():
    if request.method=="GET":
        return render_template("search.html")
    return "HELLO"

#ajax response
@app.route('/_retrievesong',methods=['POST'])
def cercasong():
    if request.method=="POST":
        name = request.form['songname']
        if len(name)==0:
            return jsonify(result="null")
        else:
            l = []

            l.extend(db.session.query(Song).filter(Song.Name.like(name)).all())
            l.extend(db.session.query(Song).filter(Song.Artist.like(name)).all())
            return jsonify(result=l)