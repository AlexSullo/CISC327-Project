'''
Required for the folder to be considered a module
'''
from flask import Flask
from . import models

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

models.db.create_all()
models.db.session.commit()
users = models.User.query.all()
print(users)