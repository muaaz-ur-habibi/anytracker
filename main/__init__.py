from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_login import LoginManager

from os import path

# creating the databases
db = SQLAlchemy()
DATA_DB_NAME = 'userdata.db'

def build_app():
    from .views import views
    from .credentials import credentials

    # secret key is same as gmail account
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "rias_gremory"
    # for sending mails
    app.config["MAIL_SERVER"] = 'smtp.gmail.com'
    app.config["MAIL_PORT"] = 465
    app.config["MAIL_USERNAME"] = 'mail.anytracker@gmail.com'
    app.config["MAIL_PASSWORD"] = 'rias_gremory'
    app.config["MAIL_USE_TLS"] = False
    app.config["MAIL_USE_SSL"] = True

    
    # configuring the database
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DATA_DB_NAME}'
    db.init_app(app=app)

    from .models import User, Graph

    with app.app_context():
        build_db()

    # creating the login manager
    login_m = LoginManager(app=app)
    login_m.login_view = 'views.home_page'
    login_m.init_app(app=app)

    @login_m.user_loader
    def load_user(id):
        return User.query.get(int(id))



    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(credentials, url_prefix="/handle_credentials")

    return app

def build_db():
    if not path.exists(f'main/{DATA_DB_NAME}'):
        db.create_all()
        print("Database created")