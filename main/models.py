from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)

    password = db.Column(db.String(200))
    name = db.Column(db.String(140), unique=True)
    
    datas = db.relationship('Graph')


class Graph(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    tracker_type = db.Column(db.String(100))

    x_values = db.Column(db.String(10000))
    y_values = db.Column(db.String(10000))

    x_axis_label = db.Column(db.String(500))
    y_axis_label = db.Column(db.String(500))

    graph_title = db.Column(db.String(200))