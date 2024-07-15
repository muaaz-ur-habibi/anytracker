"""
where views.py handles all the pages and templates,
this file handles the logins and signups
"""

from flask import Blueprint, request, render_template, flash, redirect, url_for
from .models import User
from . import db

credentials = Blueprint("credentials", __name__)

@credentials.route("/login", methods=["POST"])
def login():
    if request.method == "POST":
        email = request.form.get('emailEntry')
        password = request.form.get('passEntry')


@credentials.route("/signup", methods=["POST"])
def signup():
    email = request.form.get('emailEntry')
    password = request.form.get('passEntry')
    username = request.form.get('nameEntry')

    # pass the input data through some checks to validate their authenticity
    if len(password) < 5:
        flash("Password should be greater than 5 characters", category='error')
        return render_template('landing.html')

    elif '@' not in email or '.com' not in email or len(email) <= 4:
        flash("Please provide a valid email address", category="error")
        return render_template('landing.html')
    
    elif len(username) <= 3:
        flash("Username needs to be atleast 3 characters", category="error")
        return render_template('landing.html')

    else:
        # after all checks are passed, create the user account and add it to the database
        created_user = User(email=email, password=password, name=username)
        
        db.session.add(created_user)
        db.session.commit()

        flash("Account has been created", 'success')
        return redirect(f'/home/{username}')