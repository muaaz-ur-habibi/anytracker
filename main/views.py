from flask import Blueprint, render_template, request, flash
from .models import User, Graph
from flask_login import login_required, current_user

# necessary imports to create a graph
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigCanv
import io
from flask import Response

from . import db

views = Blueprint("views", __name__)

@views.route("/")
def home_page():
    return render_template("landing.html", logged=current_user)


@views.route("/home/<string:uname>", methods=["GET"])
@login_required
def home(uname):
    user_info = User.query.filter_by(name=uname).first()
    
    return render_template('home.html', uname=user_info, logged=current_user)
    

@views.route("<string:uname>/create_a_tracker", methods=["GET", "POST"])
@login_required
def create_a_tracker(uname):
    user_info = User.query.filter_by(name=uname).first()

    if request.method == "GET":
        return render_template('create_tracker.html', uname=user_info, logged=current_user)
    
    elif request.method == "POST":
        # get all the necessary data from form
        tracker_type = request.form.get('tracker-select')

        x_values = request.form.get('x-axis-values')
        y_values = request.form.get('y-axis-values')

        # implement a check, to check that both the values are same dimensions
        x_check = x_values.split(", ")
        y_check = y_values.split(", ")

        graph_title = request.form.get('graph-title')

        current_graph_title = Graph.query.filter_by(graph_title=graph_title).first()
        
        if len(x_check) != len(y_check):
            flash("Dimensions of added values are not equal.", 'error')
            return render_template('create_tracker.html', uname=user_info, logged=current_user)
        elif current_graph_title is not None:
            flash("A tracker already exists with that name", category="error")
            return render_template('create_tracker.html', uname=user_info, logged=current_user)
        else:
            x_axis_title = request.form.get('x-axis-label')
            y_axis_title = request.form.get('y-axis-label')

            # create the new tracker object
            new_tracker = Graph(user_id=current_user.id,
                                tracker_type=tracker_type,
                                x_values=x_values,
                                y_values=y_values,
                                x_axis_label=x_axis_title,
                                y_axis_label=y_axis_title,
                                graph_title=graph_title)
            # add the new tracker to database and commit
            db.session.add(new_tracker)
            db.session.commit()

            flash("Tracker created successfully", category="success")
            return render_template('create_tracker.html', uname=user_info, logged=current_user)


# these functions generate the graphs
@views.route('<string:uname>/<string:graph_title>/create_graph_png/plot.png')
def create_graph_png(uname, graph_title):
    user_data = User.query.filter_by(name=uname).first()
    graphs_data = Graph.query.filter_by(user_id=user_data.id, graph_title=graph_title).first()

    x_label = graphs_data.x_axis_label
    y_label = graphs_data.y_axis_label
    
    # A simple check to see if the user entered integer values or alphabetical values.
    # These two checks will return integer list if the strings can be converted to an integer
    try:
        x = graphs_data.x_values
        x = x.split(", ")
        x = [int(i) for i in x]
    except ValueError:
        x = graphs_data.x_values
        x = x.split(", ")
        x = [i for i in x]

    try:
        y = graphs_data.y_values
        y = y.split(", ")
        y = [int(i) for i in y]
    except ValueError:
        y = graphs_data.y_values
        y = y.split(", ")
        y = [i for i in y]

    graph_type = graphs_data.tracker_type

    print(graph_type)
    
    graph = create_graph(x_data=x, y_data=y, x_label=x_label, y_label=y_label, graph_type=graph_type)
    graph_pic = io.BytesIO()
    FigCanv(graph).print_png(graph_pic)

    return Response(graph_pic.getvalue(), mimetype="image/png")


def create_graph(x_data:list,
                y_data:list,
                x_label:str,
                y_label:str,
                graph_type:str):
    graph = Figure()

    # create the 3 different types of graphs

    if graph_type == "line":
        axis = graph.add_subplot(1, 1, 1)

        # actual data that is plotted
        axis.plot(x_data, y_data)
        axis.set_xlabel(xlabel=x_label)
        axis.set_ylabel(ylabel=y_label)

        return graph
    
    elif graph_type == "bar":
        axis = graph.add_subplot(1, 1, 1)

        # actual data that is plotted
        axis.bar(x=x_data, height=y_data, width=0.5, color="green")
        axis.set_xlabel(xlabel=x_label)
        axis.set_ylabel(ylabel=y_label)

        return graph


@views.route("/<string:uname>/view_trackers/<string:tracker_name>")
@login_required
def view_trackers(uname, tracker_name):
    user_info = User.query.filter_by(name=uname).first()
    graphs_data = Graph.query.filter_by(user_id=user_info.id).first()



    return render_template('view_trackers.html', uname=user_info, logged=current_user, tracker_name=tracker_name, graph_data=graphs_data)


@views.route('/<string:uname>/update_tracker/<string:tracker_name>', methods=["GET", "POST"])
@login_required
def update_tracker(uname, tracker_name):
    user_info = User.query.filter_by(name=uname).first()
    graphs_info = Graph.query.filter_by(user_id=user_info.id).first()

    if request.method == "GET":
        return render_template('update_tracker.html', uname=uname, tracker_name=tracker_name, logged=current_user, graphs_info=graphs_info)
    
    elif request.method == "POST":
        pass