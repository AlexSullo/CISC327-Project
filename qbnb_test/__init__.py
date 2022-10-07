'''
Required for the folder to be considered a module
'''
from flask import Flask
test_app = Flask(__name__)
test_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../testdb.sqlite'
test_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
