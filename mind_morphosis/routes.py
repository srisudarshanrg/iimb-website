from flask import render_template
from . import app, db

@app.route("/")
@app.route("/home")
# home is the handler for the home page
def home():
    return render_template("home.html")

@app.route("/about")
#  is the handler for the  page
def about():
    return render_template("about.html")

@app.route("/contact")
# contact is the handler for the  page
def contact():
    return render_template("contact.html")

@app.route("/education")
# education is the handler for the  page
def education():
    return render_template("education.html")

@app.route("/services")
# services is the handler for the  page
def services():
    return render_template("services.html")

@app.route("/subscription")
# subscription is the handler for the  page
def subscription():
    return render_template("subscription.html")

@app.route("/terms")
# terms is the handler for the  page
def terms():
    return render_template("terms.html")

@app.route("/tranquility")
# tranquility is the handler for the  page
def tranquility():
    return render_template("tranquility.html")

@app.route("/forum")
# forum is the handler for the  page
# @login_required
def forum():
    return render_template("forum.html")