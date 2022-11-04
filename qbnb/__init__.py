'''
Required for the folder to be considered a module
'''
from flask import Flask
from flask_login import LoginManager
import os

package_dir = os.path.dirname(
    os.path.abspath(__file__)
)

templates = os.path.join(
    package_dir, "templates"
)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'aaalsatechnologieszz11223344alsatechnologies'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.app_context().push()




