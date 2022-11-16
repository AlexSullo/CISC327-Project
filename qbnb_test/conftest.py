import os
import pytest
import time
import tempfile
import threading
from werkzeug.serving import make_server
import shutil
from qbnb import app


def pytest_sessionstart():
    '''
    Deletes the database if it exists, after copying it to a new file.
    '''
    print("Setting up testing environment...")
    db_file = 'db.sqlite'
    if os.path.exists(db_file):
        shutil.copyfile(db_file, 'BACKUP1.sqlite')
        os.remove(db_file)
        print("Database removed.")
    app.app_context().push()


def pytest_sessionfinish():
    '''
    Reset database
    '''
    os.remove('db.sqlite')
    shutil.copyfile('BACKUP1.sqlite', 'db.sqlite')
    os.remove('BACKUP1.sqlite')
    app.app_context().push()
        

base_url = 'http://127.0.0.1:{}'.format(5000)


class ServerThread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        # import necessary routes
        from qbnb import controllers
        self.srv = make_server('127.0.0.1', 5000, app)
        self.ctx = app.app_context()
        self.ctx.push()

    def run(self):
        self.srv.serve_forever()

    def shutdown(self):
        self.srv.shutdown()


@pytest.fixture(scope="session", autouse=True)
def server():
    # create a live server for testing
    # with a temporary file as database
    server = ServerThread()
    server.start()
    time.sleep(5)
    yield
    server.shutdown()
    time.sleep(2)
