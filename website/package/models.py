from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    firstname = db.Column(db.String(150))
    notes = db.relationship('Note')
    Sub=db.relationship('Submission')


class Submission(db.Model):
    Id = db.Column(db.Integer, primary_key=True)
    Data_ID = db.Column(db.Integer, unique=True)
    Title=db.column(db.String(150))
    Desc = db.Column(db.String(150))
    Pub = db.Column(db.String(150))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    