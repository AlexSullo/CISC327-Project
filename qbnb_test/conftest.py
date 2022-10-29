from qbnb import *
from qbnb.models import *
from qbnb_test import *


def open_server():
    test_db = SQLAlchemy(test_app)
    test_db.session.create_all()
    test_app.run()


open_server()
