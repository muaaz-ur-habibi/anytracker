"""
where views.py handles all the pages and templates,
this file handles the logins and signups
"""

from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user

from .models import User
from . import db

credentials = Blueprint("credentials", __name__)

@credentials.route("/login", methods=["POST"])
def login():
    print("Logging in")
    username = request.form.get('nameEntryLogin')
    password = request.form.get('passEntryLogin')

    # query the database with the username given
    user = User.query.filter_by(name=username).first()

    # if it exists
    if user != None:
        # check the password
        if user.password == password:
            # login the user
            login_user(user=user, remember=True)

            return redirect(f'/home/{username}')

        # else give an error
        else:
            flash("Incorrect password", category="error")
            return render_template('landing.html')

    # else tell them that their username doesnt exist
    else:
        flash("User does'nt exist", category='error')
        return render_template('landing.html')


@credentials.route("/signup", methods=["POST"])
def signup():
    password = request.form.get('passEntry')
    username = request.form.get('nameEntry')

    # pass the input data through some checks to validate their authenticity
    if len(password) < 5:
        flash("Password should be greater than 5 characters", category='error')
        return render_template('landing.html')
    
    elif len(username) <= 2:
        flash("Username needs to be atleast 2 characters", category="error")
        return render_template('landing.html')

    else:
        # after all checks are passed, create the user account and add it to the database
        created_user = User(password=password, name=username)

        user_exist = User.query.filter_by(name=username).first()
        
        # if the username doesnt already exist
        if user_exist == None:

            # create the user account
            db.session.add(created_user)
            db.session.commit()

            flash("Account has been created", 'success')

            # login the user
            login_user(user=created_user)

            return redirect(f'/home/{username}')

        # else return an error that the username exists
        else:
            flash("Account with that username already exists", 'error')
            return render_template('landing.html')
        

@credentials.route('/logout')
@login_required
def logout():
    logout_user()

    return redirect('/')