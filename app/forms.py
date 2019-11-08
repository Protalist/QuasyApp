from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,FileField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo

import pandas as pd

from app.models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class uploadFile(FlaskForm):
    songs = FileField("Songs",validators=[DataRequired()])

    """def validate_songs(self,songs):
        try:
            print("link")
            print(songs.data.filename)
            db = pd.read_csv(songs.data.filename, sep='\t', header=None, names=['title','artist', 'years'])
        except:
            raise ValidationError('Please use a file in this format "title \\t artist \\t years " ')"""