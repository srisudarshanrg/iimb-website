from email import message
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField
from wtforms.validators import DataRequired, Length, EqualTo

class LoginForm(FlaskForm):
    credential = StringField(label="Username or Email", validators=[DataRequired(message="This field is required.")])
    pwd = StringField(label="Password", validators=[DataRequired(message="This field is required")])
    submit = SubmitField(label="Enter")

class RegisterForm(FlaskForm):
    username = StringField(label="Username", validators=[DataRequired(message="This field is required."), Length(min=3, max=30, message="Username must be at least 3 characters long and maximum length is 30 characters.")])
    email = EmailField(label="Email", validators=[DataRequired(message="This field is required.")])
    pwd = StringField(label="Password", validators=[DataRequired(message="This field is required.")])
    pwd_confirm = StringField(label="Confirm Password", validators=[EqualTo('pwd', message="Confirm Password should be equal to Password.")])
    submit = SubmitField(label="Register")