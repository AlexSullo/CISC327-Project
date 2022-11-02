from seleniumbase import BaseCase
from unittest.mock import patch
from qbnb.models import User


def FrontEndUserTest(BaseCase):
    base_url = 'http://127.0.0.1:{}'.format(5000)
    # Login Tests
    def test_userLoginPass(self, *_):
        print("ALDEN DEMELLLLLLO")
        self.open(base_url + '/login')

        self.type("#email", "sebsemail@email.com")
        self.type("#password", "Password1!")
        self.click('input[type="submit"]')

        self.open(base_url)
        self.assert_element("#view-profile-button")