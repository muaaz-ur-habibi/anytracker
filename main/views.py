from flask import Blueprint, render_template, request

views = Blueprint("views", __name__)

@views.route("/")
def homePage():
    return render_template("landing.html")


@views.route("/home/<string:uname>", methods=["GET"])
def signUp(uname):
    
    return render_template('home.html', uname=uname)
    

@views.route('/test')
def test():

    return