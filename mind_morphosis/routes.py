from flask import render_template
from mind_morphosis.forms import LoginForm, RegisterForm
from . import app, db

@app.route("/")
@app.route("/home")
# home is the handler for the home page
def home():
    return render_template("home.html")

@app.route("/about")
#  is the handler for the about page
def about():
    return render_template("about.html")

@app.route("/contact")
# contact is the handler for the contact page
def contact():
    return render_template("contact.html")

@app.route("/education")
# education is the handler for the education page
def education():
    return render_template("education.html")

@app.route("/services")
# services is the handler for the services page
def services():
    return render_template("services.html")

@app.route("/subscription")
# subscription is the handler for the subscription page
def subscription():
    return render_template("subscription.html")

@app.route("/terms")
# terms is the handler for the terms page
def terms():
    return render_template("terms.html")

@app.route("/tranquility")
# tranquility is the handler for the tranquility page
def tranquility():
    return render_template("tranquility.html")

@app.route("/forum")
# @login_required
# forum is the handler for the forum page
def forum():
    return render_template("forum.html")

@app.route("/login")
# login is the handler for the login page
def login():
    login_form = LoginForm()
    return render_template("login.html",
                           form=login_form,
                           )

@app.route("/register")
# register is the handler for the register page
def register():
    register_form = RegisterForm()
    return render_template("register.html",
                           form=register_form,
                           )