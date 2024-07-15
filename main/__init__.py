from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from os import path

# creating the databases
db = SQLAlchemy()
DATA_DB_NAME = 'userdata.db'

def build_app():
    from .views import views
    from .credentials import credentials

    app = Flask(__name__)
    app.config["SECRET_KEY"] = "rias_gremory"
    
    # configuring the database
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DATA_DB_NAME}'
    db.init_app(app=app)

    from .models import User, Graph

    with app.app_context():
        build_db()

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(credentials, url_prefix="/handle_credentials")

    return app

def build_db():
    if not path.exists(f'main/{DATA_DB_NAME}'):
        db.create_all()
        print("Database created")