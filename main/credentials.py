"""
where views.py handles all the pages and templates,
this file handles the logins and signups
"""

from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required

from hashlib import sha256

# for the mails body
from email.message import EmailMessage

from . import build_smtp

from .models import User
from . import db

smtp = build_smtp()

credentials = Blueprint("credentials", __name__)

@credentials.route("/login", methods=["POST"])
def login():
    email = request.form.get('nameEntryLogin')
    password = request.form.get('passEntryLogin')

    # query the database with the email given
    user = User.query.filter_by(name=email).first()

    # if it exists
    if user != None:
        # check the password
        if user.password == sha256(password.encode()).hexdigest():
            # login the user
            login_user(user=user)

            return redirect(f'/home/{email}')

        # else give an error
        else:
            flash("Incorrect password", category="error")
            return render_template('landing.html')

    # else tell them that their email doesnt exist
    else:
        flash("User does'nt exist", category='error')
        return render_template('landing.html')


@credentials.route("/signup", methods=["POST"])
def signup():
    password = request.form.get('passEntry')
    email = request.form.get('nameEntry')

    # pass the input data through some checks to validate their authenticity
    if len(password) < 5:
        flash("Password should be greater than 5 characters", category='error')
        return render_template('landing.html')
    
    elif len(email) <= 2:
        flash("email needs to be atleast 2 characters", category="error")
        return render_template('landing.html')

    else:
        # after all checks are passed, create the user account and add it to the database
        created_user = User(password=sha256(password.encode()).hexdigest(), name=email)

        user_exist = User.query.filter_by(name=email).first()
        
        # if the email doesnt already exist
        if user_exist == None:

            # create the user account
            db.session.add(created_user)
            db.session.commit()

            flash("Account has been created", 'success')

            # login the user
            login_user(user=created_user)

            return redirect(f'/home/{email}')

        # else return an error that the email exists
        else:
            flash("Account with that email already exists", 'error')
            return render_template('landing.html')
        

def verification(email:str, code:int):
    smtp.sendmail("muaazarkhan@gmail.com")
    mail = EmailMessage()
    mail["Subject"] = "Signing Up: Verification"
    mail["From"] = "mail.anytracker@gmail.com"
    mail["To"] = email
    email.set_content("""
Hey there! Thanks for signing up to Anytracker. We hope you enjoy our service

Anyways here's the verification code: {code}. Thanks for your time. Have a trackable experience
""")


@credentials.route('/logout')
@login_required
def logout():
    logout_user()

    return redirect('/')