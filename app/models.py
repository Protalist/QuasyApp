from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from app import db, login


class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(64), index=True, unique=True)
    Artist = db.Column(db.String(120), index=True, unique=True)
    Year  = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return '<Song {},{},{}>'.format(self.Name,self.Artist,str(self.Year))

    def __eq__(self, other):
        if not isinstance(other, Song):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return self.Name == other.Name and self.Artist == other.Artist