from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


# Define user table
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(256), unique=True, nullable=False)
    name = db.Column(db.String(16), nullable=False)
    password = db.Column(db.String(256), nullable=False)
    notes = db.relationship('Note', order_by='Note.date.desc()')


# Define note table
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(100000), nullable=False)
    date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
