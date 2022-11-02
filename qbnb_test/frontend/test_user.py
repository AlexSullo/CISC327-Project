from seleniumbase import BaseCase
from unittest.mock import patch
from qbnb.models import User, db


class FrontEndHomePageTest(BaseCase):
    testUserInfo = {"firstName": "Automated",
                    "surname": "Testuser",
                    "email": "automatedtestuser@email.com",
                    "password": "testedPassword1!",
                    "billingAddress": "1212 Test Address",
                    "postalCode": "A1A1A1",
                    "username": "automateduser"}
    
    testUser = User(testUserInfo)
    db.session.add(testUser)
    db.session.commit()
    
    # Login Tests
    def test_userLoginPass(self, *_):
        
        base_url = 'http://127.0.0.1:{}'.format(5000)
        self.open(base_url + '/login')

        self.type("#email", "automatedtestuser@email.com")
        self.type("#password", "testedPassword1!")
        self.click('#login-button')

        self.open(base_url)
        self.assert_element(".standard-button")