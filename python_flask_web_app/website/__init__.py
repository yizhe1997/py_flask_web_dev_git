'''
Makes the website folder a pyhton app,
runs automaticaly when imported.
'''

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    #initialize flask
    app = Flask(__name__)

    #configure secret key, do not share
    app.config['SECRET_KEY'] = 'bob'

    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    #register/importing blueprints/urls to the app
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix = '/')
    app.register_blueprint(auth, url_prefix = '/')

    from .models import User, Note

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    #decorator uses the function to load the user, can use more advance searching methods by changing the func
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    return app

def create_database(app):
    
    #use path module to check if database exist
    if not path.exists('website/' + DB_NAME):
        
        #create if it does not exist
        db.create_all(app=app)
        print('Created Database')

