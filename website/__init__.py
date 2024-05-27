from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secretkey'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    db.init_app(app)

    from .routes import routes
    from .auth import auth

    app.register_blueprint(routes, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import UserDatabase

    create_database(app)

    login_mng = LoginManager()
    login_mng.login_view = 'auth.login'
    login_mng.init_app(app)

    @login_mng.user_loader  # telling login manager to use this function to load user
    def load_user(id):
        return UserDatabase.query.get(int(id))

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        app.app_context().push()
        db.create_all()
        print('Database created.')