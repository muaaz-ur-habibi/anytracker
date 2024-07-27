"""
where views.py handles all the pages and templates,
this file handles the logins and signups
"""

from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required

from hashlib import sha256


import random


from .models import User
from . import db


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
        return redirect(url_for("views.home_page"))
    
    elif len(email) <= 5 or "@" not in email or ".com" not in email:
        flash("Please enter a valid email address", category="error")
        return redirect(url_for("views.home_page"))

    else:
        # after all checks are passed, create the user account and add it to the database
        created_user = User(password=sha256(password.encode()).hexdigest(), name=email, verification_code=generate_code())

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
            return redirect(url_for("views.home_page"))
        
def generate_code():
    letters = "a b c d e f g h j k l m n o p q r s t u v w x y z A B C D E F G H I J K L M N O P Q R S T U V W X Y Z"
    letters = letters.split(" ")

    code = [letters[random.randint(0, 24)] for _ in range(0, 9)]

    code = "".join(i for i in code).lower()

    return code

@credentials.route('/logout')
@login_required
def logout():
    logout_user()

    return redirect('/')