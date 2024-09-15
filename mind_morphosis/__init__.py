from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from . import confidential

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = confidential.database_uri
app.config["SECRET_KEY"] = confidential.secret_key

from . import routes