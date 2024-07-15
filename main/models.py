from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), unique=True)
    password = db.Column(db.String(200))

    name = db.Column(db.String(140), unique=True)
    datas = db.relationship('Graphs')


class Graph(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    x_values = db.Column(db.String(10000))
    y_values = db.Column(db.String(10000))