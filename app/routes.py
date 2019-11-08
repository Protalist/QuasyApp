from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from werkzeug import secure_filename

from app import app, db
from app.models import Song, User
from app.forms import LoginForm, RegistrationForm, uploadFile

import pandas as pd
import csv
LIST_SELECTED_SONG = []
LAST_SONG = None



@app.route('/')
@app.route('/index')
@login_required
def index():
    if not acces_permission(current_user.role, 0):
        return redirect(url_for('getlist'))
    else:
        return redirect(url_for('searchsong'))
    return render_template("base.html", songs=LIST_SELECTED_SONG)


@app.route('/song')
def songs():
    songs = Song.query.all()
    return render_template('songs.html', songs=songs)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('forms_login.html', title='Sign In',songs=[], form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/searchs", methods=["GET"])
@login_required
def searchsong():
    if not acces_permission(current_user.role, 0) and not acces_permission(current_user.role, 1) :
        return redirect(url_for('index'))
    if request.method == "GET":
        return render_template("search.html", songs=LIST_SELECTED_SONG)
    return "HELLO"


# ajax response
@app.route('/_retrievesong', methods=['POST'])
def cercasong():
    if request.method == "POST":
        name = request.form['songname']
        if len(name) == 0:
            return jsonify(result="null")
        else:
            l = []
            name = "{}%".format(name)
            songsSet = set()

            l.extend(db.session.query(Song).filter(Song.Name.like(name)).all())
            l.extend(db.session.query(Song).filter(Song.Artist.like(name)).all())
            for s in l:
                songsSet.add(str(s))

            return jsonify(result=list(songsSet))


@app.route('/_addToSelected', methods=["GET"])
def addtoList():
    s = request.args.get('s', 0)
    nomeSong, artista, anno = s.split(",")
    print(nomeSong)
    print(artista)
    print(anno)
    S = Song.query.filter_by(Name=nomeSong.replace(" ", ""), Artist=artista, Year=anno).first()
    LIST_SELECTED_SONG.append(Song(Name=nomeSong.strip(), Artist=artista.strip(), Year=anno))

    return jsonify(result=True)


@app.route('/listdj', methods=['GET','POST','DELETE'])
@login_required
def getlist():
    if not acces_permission(current_user.role, 1):
        return redirect(url_for('index'))
    
    
    print("sono qui")

    if request.method=="POST":
         print("sono nel submit")
         #print(request.form["songs"])
         #print(request.files["songs"].read().decode("UTF-8"))
         v=request.files["songs"].read().decode("UTF-8").split("\n")
         print(v)
         for i in v:
             print(i[9].encode())
             j=i.split("|")
             print(j[0])
             song=Song(Name=j[0],Artist=j[1],Year=int(j[2]))
             db.session.add(song)
         db.session.commit()
    form=uploadFile()
    global  LAST_SONG
    if(len(LIST_SELECTED_SONG)>0):
        LAST_SONG = LIST_SELECTED_SONG[len(LIST_SELECTED_SONG) - 1]
    return render_template("dj.html", songs=LIST_SELECTED_SONG, length=len(LIST_SELECTED_SONG),form=form)


@app.route('/_popsong', methods=['POST'])
def pop():
    if len(LIST_SELECTED_SONG) == 0:
        return jsonify(result="null")
    LIST_SELECTED_SONG.pop(0)
    return jsonify(result=str(LIST_SELECTED_SONG[0]))


@app.route('/_update', methods=['GET'])
def updateList():
    sonsSet = []
    if len(LIST_SELECTED_SONG)<=0:
        return jsonify(result="null")
    for s in range(1,len(LIST_SELECTED_SONG)):
        sonsSet.append(str(LIST_SELECTED_SONG[s]))
    
    LAST_SONG = LIST_SELECTED_SONG[len(LIST_SELECTED_SONG)-1]
    print(sonsSet)
    if len(sonsSet)<=0:
        return jsonify(result="null")
    return jsonify(result=list(sonsSet))

@app.route('/deletesong', methods=['POST'])
def deleteallsong():
    print("sono nella delete")
    s=Song.query.all()
    print(s)
    if len(s)!=0:
        for i in s:
            db.session.delete(i)
        db.session.commit()
    return redirect(url_for("getlist"))


def acces_permission(cuser, perm):
    if (cuser == perm):
        return True
    return False

