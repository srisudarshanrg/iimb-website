from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, login_required, logout_user
from mind_morphosis.forms import LoginForm, RegisterForm
from mind_morphosis.functions import CheckHashPassword, HashPassword
from mind_morphosis.models import Users
from . import app, db

@app.route("/")
@app.route("/home")
# home is the handler for the home page
def home():
    return render_template("home.html")

@app.route("/profile")
@login_required
# profile is the handler for the user profile page
def profile():
    return render_template("profile.html")

@app.route("/about")
@login_required
# about is the handler for the about page
def about():
    return render_template("about.html")

@app.route("/contact")
@login_required
# contact is the handler for the contact page
def contact():
    return render_template("contact.html")

@app.route("/education")
@login_required
# education is the handler for the education page
def education():
    return render_template("education.html")

@app.route("/services")
@login_required
# services is the handler for the services page
def services():
    return render_template("services.html")

@app.route("/subscription")
@login_required
# subscription is the handler for the subscription page
def subscription():
    return render_template("subscription.html")

@app.route("/terms")
@login_required
# terms is the handler for the terms page
def terms():
    return render_template("terms.html")

@app.route("/tranquility")
@login_required
# tranquility is the handler for the tranquility page
def tranquility():
    return render_template("tranquility.html")

@app.route("/forum")
@login_required
# forum is the handler for the forum page
def forum():
    return render_template("forum.html")

@app.route("/login", methods=["GET", "POST"])
# login is the handler for the login page
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
                    print("logged in")
                else:
                    print("false")
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

@app.route("/register", methods=["GET", "POST"])
# register is the handler for the register page
def register():
    register_form = RegisterForm()
    
    if request.method == "POST":
        if "register" in request.form and register_form.errors == {}:
            new_user = Users(
                username=register_form.username.data,
                pwd=HashPassword(register_form.pwd.data),
                email=register_form.email.data,
            )

            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for("home"))

    return render_template("register.html",
                           form=register_form,
                           )

@app.route("/logout")
def logout():
    logout_user()
    flash(message="You have been logged out", category="info")
    return redirect(url_for('login'))