from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, ValidationError
from wtforms.validators import DataRequired, Length, EqualTo
from . import login_manager
from .models import Users

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

class LoginForm(FlaskForm):
    credential = StringField(label="Username or Email", validators=[DataRequired(message="This field is required.")])
    pwd = StringField(label="Password", validators=[DataRequired(message="This field is required")])
    submit = SubmitField(label="Enter")

class RegisterForm(FlaskForm):
    def validate_username(self, username_entered):
        check_username_exists = Users.query.filter_by(username=username_entered.data).all()
        if len(check_username_exists) > 0:
            raise ValidationError(message="This username already exists. Please choose another one.")
        
    def validate_email(self, email_entered):
        check_email_exists = Users.query.filter_by(email=email_entered.data).all()
        if len(check_email_exists) > 0:
            raise ValidationError(message="This email address already exists.")
        
    def validate_phone(self, phone_entered):
        check_phone_exists = Users.query.filter_by(phone=phone_entered.data).all()
        if len(check_phone_exists) > 0:
            raise ValidationError(message="This phone number already exists.")

    username = StringField(label="Username", validators=[DataRequired(message="This field is required."), Length(min=3, max=30, message="Username must be at least 3 characters long and maximum length is 30 characters.")])
    email = EmailField(label="Email", validators=[DataRequired(message="This field is required.")])
    pwd = StringField(label="Password", validators=[DataRequired(message="This field is required.")])
    pwd_confirm = StringField(label="Confirm Password", validators=[EqualTo('pwd', message="Confirm Password should be equal to Password.")])
    phone = StringField(label="Phone Number", validators=[DataRequired(message="This field is required.")])
    submit = SubmitField(label="Register")

class ChangeForm(FlaskForm):
    username = StringField(label="Username", validators=[DataRequired(message="This field is required."), Length(min=3, max=30, message="Username must be at least 3 characters long and maximum length is 30 characters.")])
    email = EmailField(label="Email", validators=[DataRequired(message="This field is required.")])
    phone = StringField(label="Phone Number")
    submit = SubmitField(label="Save Changes")