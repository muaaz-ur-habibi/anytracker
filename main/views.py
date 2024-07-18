from flask import Blueprint, render_template, request
from .models import User, Graph
from flask_login import login_required, current_user

from . import db

views = Blueprint("views", __name__)

@views.route("/")
def home_page():
    return render_template("landing.html", logged=current_user)


@views.route("/home/<string:uname>", methods=["GET"])
@login_required
def home(uname):
    user_info = User.query.filter_by(name=uname).first()
    print(user_info.datas)
    
    return render_template('home.html', uname=user_info, logged=current_user)
    

@views.route("<string:uname>/create_a_tracker", methods=["GET", "POST"])
@login_required
def create_a_tracker(uname):
    user_info = User.query.filter_by(name=uname).first()
    print(user_info)

    if request.method == "GET":
        return render_template('create_tracker.html', uname=user_info, logged=current_user)
    
    elif request.method == "POST":
        tracker_type = request.form.get('tracker-select')

        x_values = request.form.get('x-axis-values')
        y_values = request.form.get('y-axis-values')

        x_axis_title = request.form.get('x-axis-label')
        y_axis_title = request.form.get('y-axis-label')

        graph_title = request.form.get('graph-title')

        new_tracker = Graph(user_id=current_user.id,
                            tracker_type=tracker_type,
                            x_values=x_values,
                            y_values=y_values,
                            x_axis_label=x_axis_title,
                            y_axis_label=y_axis_title,
                            graph_title=graph_title)
        
        db.session.add(new_tracker)
        db.session.commit()

        return "interesting"


@views.route("/<string:uname>/view_trackers/<string:tracker_name>")
@login_required
def view_trackers(uname, tracker_name):
    user_info = User.query.filter_by(name=uname).first()

    
    
    return render_template('view_trackers.html', uname=user_info)