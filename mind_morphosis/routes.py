import datetime
import random
from flask import flash, redirect, render_template, request, session, url_for
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
        "pwd": user_details_row.pwd,
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
            pwd_entered = request.form.get("del_acc_password")
            
            if CheckHashPassword(user_details["pwd"], pwd_entered):
                user_to_delete_row = Users.query.filter_by(id=current_user.id).first()
                db.session.delete(user_to_delete_row)
                db.session.commit()

                flash(message="Your account has been deleted", category="info")

                return redirect(url_for('login'))
            else:
                flash(message="Incorrect Password", category="danger")     
                return redirect(url_for('profile'))
            
        elif "changePassword" in request.form:
            pwd_entered = request.form.get("change-pwd")

            if CheckHashPassword(user_details["pwd"], pwd_entered):
                return redirect(url_for('reset_pwd'))
            else:
                flash(message="Incorrect Password", category="danger")
                return redirect(url_for('profile'))

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
        if login_form.validate_on_submit() and login_form.errors == {}:
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

            else:
                flash(message="This user does not exist. Would you like to register?", category="info")

        if login_form.validate_on_submit() and login_form.errors != {}:
            for error in login_form.errors.values():
                return flash(message=error, category="danger")
            
        elif "forgotPassword" in request.form:
            smtp = smtplib.SMTP("smtp.gmail.com", 587)

            otp = str(random.randint(0, 999999))

            to_email_address = request.form.get("forgot-pwd")
            session['email'] = to_email_address

            msg = f"OTP for {to_email_address} from MindMorphosis is {otp}"

            smtp.starttls()
            smtp.login(user=email, password=app_pwd)
            smtp.sendmail(from_addr=email, to_addrs=to_email_address, msg=msg)

            flash(message="An OTP has been sent to your mail. Please check the OTP and type in below.", category="info")

            session['otp'] = otp

            return redirect(url_for('otp_confirm'))

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

    if "email" in session:
        session.pop("email")

    if "otp" in session:
        session.pop("otp")
        
    flash(message="You have been logged out", category="info")
    return redirect(url_for('login'))

# reset_pwd is the handler for the reset password page
@app.route("/reset-pwd", methods=["GET", "POST"])
def reset_pwd():
    email = session.get("email")

    user_details_row_alternative = Users.query.filter_by(email=email).first()

    if current_user.is_authenticated:
        user_details_row = Users.query.filter_by(id=current_user.id).first()
        if request.method == "POST":
            pwd_entered = request.form.get("pwd")
            pwd_entered_confirm = request.form.get("pwd-confirm")
            if pwd_entered == pwd_entered_confirm:
                new_pwd = HashPassword(pwd_entered)
                user_details_row.pwd = new_pwd

                db.session.commit()
                flash(message="Your password has been changed successfully!", category="success")
                return redirect(url_for('profile'))                
            else:
                flash(message="Password should be same as confirmed password.", category="danger")

                return render_template("reset-pwd.html")   
            
                     
    elif not current_user.is_authenticated and user_details_row_alternative:
        if request.method == "POST":
            pwd_entered = request.form.get("pwd")
            pwd_entered_confirm = request.form.get("pwd-confirm")
            if pwd_entered == pwd_entered_confirm:
                new_pwd = HashPassword(pwd_entered)
                user_details_row_alternative.pwd = new_pwd

                db.session.commit()
                flash(message="Your password has been changed successfully!", category="success")
                session.pop("email")
                return redirect(url_for('profile'))
            else:
                flash(message="Password should be same as confirmed password.", category="danger")

                return render_template("reset-pwd.html")
        
    else:
        flash(message="Cannot access reset password page without being logged in or using forgot password feature. While using forgot password feature, email you enter must be same as the email you used when you registered.", category="danger")
        return redirect(url_for('login'))
    
    return render_template("reset-pwd.html")
        

@app.route("/confirm-otp", methods=["GET", "POST"])
def otp_confirm():
    if request.method == "POST":
        otp = session.get("otp")
        if otp:
            otp_entered = request.form.get("otp")
            if otp == otp_entered:
                flash(message="OTP verification complete. You can reset your password here.", category="success")
                return redirect(url_for('reset_pwd'))
            else:
                flash(message="Invalid OTP. Try again.", category="danger")
        session.pop("otp")

    return render_template("otp-confirm.html")