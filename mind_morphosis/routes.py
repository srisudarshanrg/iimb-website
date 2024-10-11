import datetime
import random
from flask import flash, redirect, render_template, request, session, url_for
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
    if "admin" in session:
        admin = session.get("admin")
    else:
        admin=False

    return render_template("home.html", admin=admin)

# profile is the handler for the user profile page
@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    user_details_row = Users.query.filter_by(id=current_user.id).first()

    if user_details_row.subscription != None:
        subscription_choice = user_details_row.subscription
    else:
        subscription_choice = "No subscription subscribed for now"

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
        subscription_expire = "--"

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

    if "admin" in session:
        admin = session.get("admin")
    else:
        admin=False

    return render_template("profile.html", user_details=user_details, change=change_form, admin=admin)

# about is the handler for the about page
@app.route("/about")
@login_required
def about():
    if "admin" in session:
        admin = session.get("admin")
    else:
        admin=False
    return render_template("about.html", admin=admin)

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

    if "admin" in session:
        admin = session.get("admin")
    else:
        admin=False

    return render_template("contact.html", admin=admin)

# education is the handler for the education page
@app.route("/education")
@login_required
def education():
    if "admin" in session:
        admin = session.get("admin")
    else:
        admin=False
    return render_template("education.html", admin=admin)

# services is the handler for the services page
@app.route("/services")
@login_required
def services():
    if "admin" in session:
        admin = session.get("admin")
    else:
        admin=False
    return render_template("services.html", admin=admin)

# subscription is the handler for the subscription page
@app.route("/subscription")
@login_required
def subscription():
    if "admin" in session:
        admin = session.get("admin")
    else:
        admin=False
    return render_template("subscription.html", admin=admin)

# terms is the handler for the terms page
@app.route("/terms")
@login_required
def terms():
    if "admin" in session:
        admin = session.get("admin")
    else:
        admin=False
    return render_template("terms.html", admin=admin)

# tranquility is the handler for the tranquility page
@app.route("/tranquility")
@login_required
def tranquility():
    if "admin" in session:
        admin = session.get("admin")
    else:
        admin=False
    return render_template("tranquility.html", admin=admin)

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

        forum_count = user_details.forum_msg
        forum_count += 1

        user_details.forum_msg = forum_count

        db.session.commit()
        
        return redirect(url_for('forum'))

    if "admin" in session:
        admin = session.get("admin")
    else:
        admin=False
    return render_template("forum.html", msgs=user_msg_row, admin=admin)

@app.route("/admin", methods=["GET", "POST"])
@login_required
def admin():
    if "admin" in session:
        admin = session.get("admin")
    else:
        admin=False
        flash(message="You have to be an admin to access the admin page.", category="info")
        return redirect(url_for("home"))

    users = Users.query.filter_by().all()

    user_list = []

    for user in users:
        if user.subscription == None:
            subscription_option = "None"
            subscription_expire = "--"
        else:
            subscription_option = user.subscription
            subscription_expire = user.subscription_expire.strftime("%d %B %Y")

        join_date = user.join_date.strftime("%d %B %Y")
        
        user_dict = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "phone": user.phone,
            "join_date": join_date,
            "subscription": subscription_option,
            "subscription_expire": subscription_expire,
            "forum": user.forum_msg,
        }

        user_list.append(user_dict)
    
    sessions = Session.query.filter_by().all()

    sessions_list = []

    for session_individual in sessions:
        session_date = session_individual.session_date.strftime("%d %B %Y")
        session_time_start = session_individual.session_time_start.strftime("%H:%M")
        session_time_end = session_individual.session_time_end.strftime("%H:%M")
        
        session_dict = {
            "id": session_individual.id,
            "session_user": session_individual.session_user,
            "session_date": session_date,
            "session_time_start": session_time_start,
            "session_time_end": session_time_end,
        }

        sessions_list.append(session_dict)

    if len(sessions_list) == 0:
        session_exist = False
    else:
        session_exist = True

    if request.method == "POST":
        if "deleteUser" in request.form:
            username = request.form.get("user_delete")
            reason = request.form.get("user_delete_reason")

            if username == "sudarshan_raptor":
                flash(message=f"Cannot delete admin account {username}", category="danger")
                return redirect(url_for('admin'))

            user = Users.query.filter_by(username=username).first()
            
            if user:
                db.session.delete(user)
                db.session.commit()

                msg = f"Your account on MindMorphosis has been deleted. \n Reason: {reason}."

                smtp = smtplib.SMTP("smtp.gmail.com", 587)

                smtp.starttls()
                smtp.login(user=email, password=app_pwd)
                smtp.sendmail(from_addr=email, to_addrs=user.email, msg=msg)

                flash(message=f"User with username '{username}' has been deleted and {username} has been notified via email", category="info")

                return redirect(url_for('admin'))
            else:
                flash(message=f"User with username '{username}' doesn't exist in database", category="danger")

        elif "deleteSession" in request.form:
            username = request.form.get("session_delete")
            reason = request.form.get("session_delete_reason")

            session_required = Session.query.filter_by(session_user=username).first()

            if session_required:
                db.session.delete(session_required)
                db.session.commit()

                session_date = session_required.session_date.strftime("%d %B %Y")
                session_time_start = session_required.session_time_start.strftime("%H: %M")
                session_time_end = session_required.session_time_end.strftime("%H: %M")

                msg = f"Your session with MindMorphosis on {session_date} from {session_time_start} to {session_time_end} has been cancelled. \n Reason: {reason}"

                smtp = smtplib.SMTP("smtp.gmail.com", 587)

                smtp.starttls()
                smtp.login(user=email, password=app_pwd)
                smtp.sendmail(from_addr=email, to_addrs=user.email, msg=msg)

                flash(f"Session with {username} has been cancelled and {username} has been notified via email", category="info")

                return redirect(url_for('admin'))
            else:
                flash(f"Session with {username} has not been booked yet and does not exist", category="danger")
    
    return render_template("admin.html", admin=admin, users=user_list, sessions=sessions_list, session_exist=session_exist)

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
                    if credential_check_username.email == "srisudarshanrg@gmail.com":
                        session["admin"] = True
                    flash("You have been logged in successfully", category="success")
                    return redirect(url_for("home"))
                else:
                    flash("Incorrect credentials", category="danger")

            elif credential_check_email:
                if CheckHashPassword(credential_check_email.pwd, pwd_entered):
                    login_user(credential_check_email)
                    if credential_check_email.email == "srisudarshanrg@gmail.com":
                        session["admin"] = True
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

    if "admin" in session:
        session.pop("admin")
        
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