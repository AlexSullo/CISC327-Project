from seleniumbase import BaseCase
from qbnb_test.conftest import base_url
from unittest.mock import patch
from qbnb.models import User

def FrontEndUserTest(BaseCase):

    # Login Tests
    def userLoginPass(self, *_):
        self.open(base_url+ '/login')

        self.type("#email", "sebsemail@email.com")
        self.type("#password", "Password1!")
        self.click('input[type="submit"]')

        self.open(base_url)
        self.assert_element("#view-profile-button")