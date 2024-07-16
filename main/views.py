from flask import Blueprint, render_template, request
from flask_login import login_required

views = Blueprint("views", __name__)

@views.route("/")
def home_page():
    return render_template("landing.html")


@views.route("/home/<string:uname>", methods=["GET"])
@login_required
def home(uname):
    
    return render_template('home.html', uname=uname)
    

@views.route("<string:uname>/create_a_tracker")
@login_required
def create_a_tracker(uname):

    return render_template('create_tracker.html', uname=uname)