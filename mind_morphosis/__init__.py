from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from . import confidential_info

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = confidential_info.database_uri
app.config["SECRET_KEY"] = confidential_info.secret_key
app.app_context().push()

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message = "Login is required to access this page."
login_manager.login_message_category = "info"

bcrypt = Bcrypt(app)

from . import routes