from . import db, login_manager

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

class Users(db.Model):
    id = db.Column(db.Integer(), primary_key=True, nullable=False)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email = db.Column(db.String(), nullable=False, unique=True)
    pwd = db.Column(db.String(), nullable=False)
    age = db.Column(db.Integer(), nullable=False)