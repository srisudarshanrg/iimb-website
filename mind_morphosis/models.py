from flask_login import UserMixin
from . import db, login_manager

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True, nullable=False)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email = db.Column(db.String(), nullable=False, unique=True)
    pwd = db.Column(db.String(), nullable=False)
    join_date = db.Column(db.DateTime(), nullable=False)
    subscription_id = db.Column(db.Integer(), db.ForeignKey("subscription.id"))
    subscription_expire = db.Column(db.DateTime())
    subscription = db.relationship("Subscription", backref="subscription", lazy=True, foreign_keys=[subscription_id])

class Subscription(db.Model):
    id = db.Column(db.Integer(), primary_key=True, nullable=False)
    subscription_options = db.Column(db.String(), nullable=False, unique=True)

class Session(db.Model):
    id = db.Column(db.Integer(), primary_key=True, nullable=False)
    session_user = db.Column(db.Integer(), db.ForeignKey("users.id"), nullable=False)
    session_date = db.Column(db.DateTime(), nullable=False)
    session_time_start = db.Column(db.DateTime(), nullable=False)
    session_time_end = db.Column(db.DateTime(), nullable=False)
    user = db.relationship("Users", backref="session_user", lazy=True, foreign_keys=[session_user])