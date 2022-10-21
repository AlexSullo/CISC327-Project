'''
Required for the folder to be considered a module
'''
from flask import Flask
from flask_login import LoginManager


def create_app():
    '''
    Starts up the app
    '''
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'aaalsatechnologieszz11223344alsatechnologies'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../db.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    return app


app = create_app()