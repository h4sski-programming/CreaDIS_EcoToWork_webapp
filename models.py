from app import db
from flask_login import UserMixin
from sqlalchemy import func


class Activity(db.Model):
    __tablename__ = 'activity'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    distance = db.Column(db.Integer)
    date_of_activity = db.Column(db.Date(), unique=True)
    activity_type = db.Column(db.String(150))
    date_of_submit = db.Column(
        db.DateTime(timezone=True), default=func.now())


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    role = db.Column(db.String(100), default='member')
    activity = db.relationship('Activity')
