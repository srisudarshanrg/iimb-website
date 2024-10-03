import datetime
from flask import flash, redirect, render_template, request, url_for
from flask.cli import F
from flask_login import current_user, login_user, login_required, logout_user
from .forms import ChangeForm, LoginForm, RegisterForm
from .functions import CheckHashPassword, HashPassword
from .models import Forum, Session, Subscription, Users
from .confidential_info import email, app_pwd
from . import app, db
import smtplib

# home is the handler for the home page
@app.route("/")
@app.route("/home")
@login_required
def home():
    return render_template("home.html")

# profile is the handler for the user profile page
@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    user_details_row = Users.query.filter_by(id=current_user.id).first()

    subscription_choice_row = Subscription.query.filter_by(id=user_details_row.subscription_id).first()

    if subscription_choice_row:
        subscription_choice = subscription_choice_row.subscription_options
    else:
        subscription_choice = "No subscriptions subscribed for now"

    sessions = Session.query.filter_by(id=current_user.id).all()

    if sessions:
        sessions = sessions
    else:
        sessions = "No sessions booked for now"

    join_date = user_details_row.join_date
    join_date = join_date.strftime("%d %B %Y")

    subscription_expire = user_details_row.subscription_expire

    if subscription_expire:
        subscription_expire = subscription_expire.strftime("%d %B %Y")
    else:
        subscription_expire = ""

    user_details = {
        "id": user_details_row.id,
        "username": user_details_row.username,
        "email": user_details_row.email,
        "phone": user_details_row.phone,
        "join_date": join_date,
        "subscription": subscription_choice,
        "subscription_expire": subscription_expire,
        "sessions": sessions,
    }

    change_form = ChangeForm()

    if request.method == "POST":
        if change_form.validate_on_submit() and change_form.errors == {}:
            user_to_change_row = Users.query.filter_by(username=user_details_row.username).first()
            user_to_change_row.username = change_form.username.data
            user_to_change_row.email = change_form.email.data
            user_to_change_row.phone = change_form.phone.data

            db.session.commit()
            
            flash(message="User details have been updated!", category="success")

            print("hello")

            return redirect(url_for('profile'))
        
        elif "deleteConfirm" in request.form:
            user_to_delete_row = Users.query.filter_by(id=current_user.id).first()
            db.session.delete(user_to_delete_row)
            db.session.commit()

            flash(message="Your account has been deleted", category="info")

            return redirect(url_for('login'))            

    return render_template("profile.html", user_details=user_details, change=change_form)

# about is the handler for the about page
@app.route("/about")
@login_required
def about():
    return render_template("about.html")

# contact is the handler for the contact page
@app.route("/contact", methods=["GET", "POST"])
@login_required
def contact():
    if request.method == "POST":
        email_address = request.form.get("email")
        msg = request.form.get("msg")

        smtp = smtplib.SMTP("smtp.gmail.com", 587)

        smtp.starttls()
        smtp.login(user=email, password=app_pwd)
        smtp.sendmail(from_addr=email, to_addrs=email_address, msg=msg)
        
        flash(message="An email has been sent to notify the respective people about your concern.", category="success")

        return render_template("contact.html")

    return render_template("contact.html")

# education is the handler for the education page
@app.route("/education")
@login_required
def education():
    return render_template("education.html")

# services is the handler for the services page
@app.route("/services")
@login_required
def services():
    return render_template("services.html")

# subscription is the handler for the subscription page
@app.route("/subscription")
@login_required
def subscription():
    return render_template("subscription.html")

# terms is the handler for the terms page
@app.route("/terms")
@login_required
def terms():
    return render_template("terms.html")

# tranquility is the handler for the tranquility page
@app.route("/tranquility")
@login_required
def tranquility():
    return render_template("tranquility.html")

# forum is the handler for the forum page
@app.route("/forum", methods=["GET", "POST"])
@login_required
def forum():
    user_details = Users.query.filter_by(id=current_user.id).first()
    username = user_details.username

    user_msg_row = Forum.query.filter_by().all()

    if request.method == "POST":
        msg = request.form.get("msg")
        new_msg = Forum(
            msg=msg,
            msg_user=username,
        )

        db.session.add(new_msg)
        db.session.commit()

        return redirect(url_for('forum'))

    return render_template("forum.html", msgs=user_msg_row)

# login is the handler for the login page
@app.route("/login", methods=["GET", "POST"])
def login():
    login_form = LoginForm()

    if request.method == "POST":
        if "login" in request.form and login_form.errors == {}:
            credential = login_form.credential.data
            pwd_entered = login_form.pwd.data

            credential_check_username = Users.query.filter_by(username=credential).first()
            credential_check_email = Users.query.filter_by(email=credential).first()

            if credential_check_username:
                if CheckHashPassword(credential_check_username.pwd, pwd_entered):
                    login_user(credential_check_username)
                    flash("You have been logged in successfully", category="success")
                    return redirect(url_for("home"))
                else:
                    flash("Incorrect credentials", category="danger")

            elif credential_check_email:
                if CheckHashPassword(credential_check_email.pwd, pwd_entered):
                    login_user(credential_check_email)
                    print("logged in")
                    flash("You have been logged in successfully", category="success")
                    return redirect(url_for("home"))
                else:
                    flash("Incorrect credentials", category="danger")

    return render_template("login.html",
                           form=login_form,
                           )

# register is the handler for the register page
@app.route("/register", methods=["GET", "POST"])
def register():
    register_form = RegisterForm()
    
    if request.method == "POST":
        if register_form.validate_on_submit() and register_form.errors == {}:
            join_date = datetime.datetime.now()
            new_user = Users(
                username=register_form.username.data,
                pwd=HashPassword(register_form.pwd.data),
                email=register_form.email.data,
                phone=register_form.phone.data,
                join_date=join_date,
            )

            db.session.add(new_user)
            db.session.commit()

            login_user(new_user)

            return redirect(url_for("home"))
        
        if register_form.errors != {}:
            for error in register_form.errors.values():
                flash(message=f"{error}", category="danger")

    return render_template("register.html",
                           form=register_form,
                           )

# logout is the handler for handling logout option
@app.route("/logout")
def logout():
    logout_user()
    flash(message="You have been logged out", category="info")
    return redirect(url_for('login'))