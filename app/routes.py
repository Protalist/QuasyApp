from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from app import app, db
from app.models import Song, User
from app.forms import LoginForm, RegistrationForm

LIST_SELECTED_SONG = []
LAST_SONG = None


@app.route('/')
@app.route('/index')
def index():
    if (len(LIST_SELECTED_SONG) == 0):
        return "Hello, World!"
    else:
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
    return render_template('forms_login.html', title='Sign In', form=form)


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
    if acces_permission(current_user.role, 1):
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
    LIST_SELECTED_SONG.append(str(S))

    return jsonify(result=True)


@app.route('/listdj', methods=['GET'])
@login_required
def getlist():
    if acces_permission(current_user.role, 1):
        return redirect(url_for('index'))
    if len(LIST_SELECTED_SONG) == 0:
        for i in range(0, 4):
            LIST_SELECTED_SONG.append(Song(Name="song" + str(i), Artist="Artist" + str(i), Year=i))
        # print(LIST_SELECTED_SONG[i])
        LAST_SONG = LIST_SELECTED_SONG[len(LIST_SELECTED_SONG) - 1];
    return render_template("dj.html", songs=LIST_SELECTED_SONG, length=len(LIST_SELECTED_SONG))


@app.route('/_popsong', methods=['POST'])
def pop():
    if len(LIST_SELECTED_SONG) == 1:
        return jsonify(result="null")
    LIST_SELECTED_SONG.pop(0)
    return jsonify(result=str(LIST_SELECTED_SONG[0]))


@app.route('/_update', methods=['GET'])
def updateList():
    find = False
    sonsSet = set()
    for s in LIST_SELECTED_SONG:
        if LAST_SONG == s:
            find = True
        if not find:
            continue
        if (find == True):
            sonsSet.add(str(s))
    if (sonsSet == None):
        return jsonify(result="null")
    LAST_SONG = LIST_SELECTED_SONG(len(LIST_SELECTED_SONG))
    return jsonify(result=list(sonsSet))


def acces_permission(cuser, perm):
    if (cuser == perm):
        return True
    return False
