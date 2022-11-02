import os
import pytest
import time
import tempfile
import threading
from werkzeug.serving import make_server
from qbnb import app
from qbnb.models import *
from qbnb_test import *


def pytest_sessionstart():
    '''
    Deletes the database if it exists, after copying it to a new file.
    '''
    print("Setting up testing environment...")
    db_file = 'db.sqlite'
    if os.path.exists(db_file):
        os.system('copy ' + db_file + " db_copy.sqlite")
        # os.remove(db_file)
    app.app_context().push()


def pytest_sessionfinish():
    '''
    When
    '''


base_url = 'http://127.0.0.1:{}'.format(8081)


class ServerThread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.srv = make_server('127.0.0.1', 8081, app)
        self.ctx = app.app_context()
        self.ctx.push()

    def run(self):
        print("Server running...")
        self.srv.serve_forver()

    def shutdown(self):
        self.srv.shutdown()


@pytest.fixture(scope="session", autouse=True)
def server():
    server = ServerThread()
    server.start()
    time.sleep(5)
    yield
    server.shutdown()
    time.sleep(2)