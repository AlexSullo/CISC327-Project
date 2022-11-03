import os
import pytest
import time
import tempfile
import threading
from werkzeug.serving import make_server
from qbnb import app


def pytest_sessionstart():
    '''
    Deletes the database if it exists, after copying it to a new file.
    '''
    print("Setting up testing environment...")
    db_file = 'db.sqlite'
    if os.path.exists(db_file):
        os.system('copy ' + db_file + " db_copy.sqlite")
        print("Database copied.")
        os.remove(db_file)
        print("Database removed.")
    app.app_context().push()
    print("App context pushed.")


def pytest_sessionfinish():
    '''
    Reset database
    '''
    print("Tearing down testing environment...")
    db_file = 'db.sqlite'
    os.remove(db_file)
    print("Testing Database removed.")
    os.system('copy db_copy.sqlite db.sqlite')
    print("Original database copied to db.sqlite.")
    time.sleep(2)
    os.remove('db_copy.sqlite')
    print("Database copy removed.")
    app.app_context().push()
    print("App context pushed.")
        

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
