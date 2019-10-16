from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(64), index=True, unique=True)
    Artist = db.Column(db.String(120), index=True, unique=True)
    Year  = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return '<User {}>'.format(self.username)