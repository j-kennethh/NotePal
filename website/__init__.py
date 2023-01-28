from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Initialise the database
db = SQLAlchemy()
DB_NAME = 'database.db'


def create():
    # Configure the application
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '9aa688fa374e4b33be6275fb9892dcc3'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    # Register authentication and view blueprints
    from .auth import auth
    app.register_blueprint(auth, url_prefix='/')

    from .view import view
    app.register_blueprint(view, url_prefix='/')

    # Ensure database is defined and create database
    from .model import User, Note
    with app.app_context():
        db.create_all()

    # Initialise the login manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'error'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app
