'''
Required for the folder to be considered a module
'''
from flask import Flask
import os


package_dir = os.path.dirname(
    os.path.abspath(__file__)
)
templates = os.path.join(
    package_dir, "templates"
)

app = Flask(__name__)
db_string = os.getenv('db_string')
if db_string:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_string
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'alsatechnologiessecretkeythatissecretandstuff1123'
app.app_context().push()




