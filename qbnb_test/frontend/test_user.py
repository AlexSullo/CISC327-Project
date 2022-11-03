from seleniumbase import BaseCase
from unittest.mock import patch
from qbnb.models import User, db
import random


class FrontEndHomePageTest(BaseCase):
    
    testUserInfo = {"firstName": "Automated",
                    "surname": "Testuser",
                    "email": "automatedtestuser@email.com",
                    "password": "testedPassword1!",
                    "billingAddress": "1212 Test Address",
                    "postalCode": "A1A1A1",
                    "username": "automateduser"}
    
    testUser = User(testUserInfo)
    testUser.billingAddress = testUserInfo["billingAddress"]
    db.session.add(testUser)
    db.session.commit()
    
    # Login Tests
    # def test_userLoginPass(self, *_):
        
    #     base_url = 'http://127.0.0.1:{}'.format(5000)
    #     self.open(base_url + '/login')

    #     self.type("#email", "automatedtestuser@email.com")
    #     self.type("#password", "testedPassword1!")
    #     self.click('#login-button')

    #     self.open(base_url)
    #     self.assert_element(".standard-button")

    '''
    User Updating Tests (Sebastian Deluca #20250909)
    email, username, billingaddress, and postalcode.

    Uses 3 Blackbox Testing Methods:
    - Input Partition Testing
    - Systematic Shotgun Testing
    - Boundary Testing

    Specification R3_1 cannot be tested as there are no possible fields to
    modify such data on the profile editing page.
    
    EMAIL: uses Input Partition (Meets Regex or Doesn't Meet Regex) (1)
    
    Partitions:
        - Invalid Regex
        - Valid Regex
    '''
    def test_userUpdateEmailFail(self, *_):
        '''
        Test Case of Updating User email Where It Fails because of an
        invalid email.
        '''

        testUser = db.session.query(User) \
            .filter_by(email="automatedtestuser@email.com").first()
        base_url = 'http://127.0.0.1:{}'.format(5000)
        self.open(base_url + "/profile/" + str(testUser.id))

        # SIGNING IN
        self.type("#email", "automatedtestuser@email.com")
        self.type("#password", "testedPassword1!")
        self.click('#login-button')
        self.open(base_url + "/profile/" + str(testUser.id))
        
        self.click("#edit-profile-info")

        # Editing User Info
        self.type("#email", "thisemaildoesnotwork@@email.com")
        self.click("#submit-edits")
        self.save_screenshot('updateemail_regexfail', 'test_screenshots')
        url = self.get_current_url()
        self.assert_false(url == (base_url + "/profile/" + str(testUser.id)))
        print("EMAIL HAS NOT CHANGED BECAUSE IT IS INVALID.")

    def test_userUpdateEmailPass(self, *_):
        '''
        Test Case of updating user email where it passes.
        ''' 
        testUser = db.session.query(User) \
            .filter_by(email="automatedtestuser@email.com").first()
        base_url = 'http://127.0.0.1:{}'.format(5000)
        self.open(base_url + "/profile/" + str(testUser.id))

        # SIGNING IN
        self.type("#email", "automatedtestuser@email.com")
        self.type("#password", "testedPassword1!")
        self.click('#login-button')
        self.open(base_url + "/profile/" + str(testUser.id))
        
        self.click("#edit-profile-info")

        # Editing User Info
        self.type("#email", "automatedworkingemail@email.com")
        self.click("#submit-edits")
        self.assert_text("automatedworkingemail@email.com", "#email")
        self.scroll_to_bottom()
        self.save_screenshot('updateemail_pass', 'test_screenshots')
        print("EMAIL HAS CHANGED.")

    '''
    USERNAME: uses Systematic Shotgun Testing & Boundary Testing (2&3)

    Partitions: 
        - Randomly generated (fails regex: space at front) SST
        - Randomly generated (fails regex: special character) SST
        - Randomly generated (fails specification: too short) SST/BT
        - Randomly generated (fails specification: too long) SST/BT
        - Randomly generated (passes Regex) SST

    NOTE: USERNAME BEING EMPTY CANNOT BE TESTED. IF THE USERNAME
          FIELD IS EMPTY UPON SUBMISSION OF THE FORM, THE USERNAME
          WILL NOT CHANGE BY DESIGN.
        
    '''
    
    def test_userUpdateUsernameFailSpace(self, *_):
        '''
        Test case of updating user username where it fails
        because the username does not match RegEx because it
        has a space as a prefix
        '''
        testUser = db.session.query(User) \
            .filter_by(email="automatedworkingemail@email.com").first()
        base_url = 'http://127.0.0.1:{}'.format(5000)
        self.open(base_url + "/profile/" + str(testUser.id))

        # SIGNING IN
        self.type("#email", "automatedworkingemail@email.com")
        self.type("#password", "testedPassword1!")
        self.click('#login-button')
        self.open(base_url + "/profile/" + str(testUser.id))
        
        self.click("#edit-profile-info")

        # Generate a random username
        choicesStr = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        choicesStr += '0123456789!#@-'
        usernameLen = random.randint(8, 16)
        rngUsername = ' '  # The randomly-generated password
        for x in range(usernameLen):
            val = random.randint(1, len(choicesStr))
            key = choicesStr[val - 1]
            rngUsername += key

        # Editing User Info
        self.type("#username", rngUsername)
        self.click("#submit-edits")
        self.save_screenshot('updateusername_spacefail', 'test_screenshots')
        url = self.get_current_url()
        self.assert_false(url == (base_url + "/profile/" + str(testUser.id)))
        print("USERNAME HAS NOT CHANGED AS IT WAS INVALID.")

    def test_userUpdateUsernameFailSpecial(self, *_):
        '''
        Test case of updating user username where it fails
        because the username does not match RegEx because it
        has a special character in the middle
        '''
        testUser = db.session.query(User) \
            .filter_by(email="automatedworkingemail@email.com").first()
        base_url = 'http://127.0.0.1:{}'.format(5000)
        self.open(base_url + "/profile/" + str(testUser.id))

        # SIGNING IN
        self.type("#email", "automatedworkingemail@email.com")
        self.type("#password", "testedPassword1!")
        self.click('#login-button')
        self.open(base_url + "/profile/" + str(testUser.id))
        
        self.click("#edit-profile-info")

        # Generate a random username
        choicesStr = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        choicesStr += '0123456789!#@-'
        usernameLen = random.randint(8, 16)
        rngUsername = ''  # The randomly-generated password
        for x in range(usernameLen):
            if x == usernameLen // 2:
                rngUsername += "!"
            else:
                val = random.randint(1, len(choicesStr))
                key = choicesStr[val - 1]
                rngUsername += key

        # Editing User Info
        self.type("#username", rngUsername)
        self.click("#submit-edits")
        self.save_screenshot('updateusername_spcharfail', 'test_screenshots')
        url = self.get_current_url()
        self.assert_false(url == (base_url + "/profile/" + str(testUser.id)))
        print("USERNAME HAS NOT CHANGED AS IT WAS INVALID")

    def test_userUpdateUsernameFailShort(self, *_):
        '''
        Test case of updating user username where it fails
        because the username does not match RegEx because it
        is too short
        '''
        testUser = db.session.query(User) \
            .filter_by(email="automatedworkingemail@email.com").first()
        base_url = 'http://127.0.0.1:{}'.format(5000)
        self.open(base_url + "/profile/" + str(testUser.id))

        # SIGNING IN
        self.type("#email", "automatedworkingemail@email.com")
        self.type("#password", "testedPassword1!")
        self.click('#login-button')
        self.open(base_url + "/profile/" + str(testUser.id))
        
        self.click("#edit-profile-info")

        # Generate a random username
        choicesStr = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        usernameLen = 2
        rngUsername = ''  # The randomly-generated password
        for x in range(usernameLen):
            val = random.randint(1, len(choicesStr))
            key = choicesStr[val - 1]
            rngUsername += key

        # Editing User Info
        self.type("#username", rngUsername)
        self.click("#submit-edits")
        self.save_screenshot('updateusername_shortfail', 'test_screenshots')
        url = self.get_current_url()
        self.assert_false(url == (base_url + "/profile/" + str(testUser.id)))
        print("USERNAME HAS NOT CHANGED AS IT WAS INVALID")

    def test_userUpdateUsernameFailLong(self, *_):
        '''
        Test case of updating user username where it fails
        because the username does not match RegEx because it
        is too long

        NOTE: THIS TEST WILL FAIL IF TESTED ON A BROWSER WITHOUT
              HTML5 SUPPORT. CHROME HAS HTML5 SUPPORT, SO IT
              PHYSICALLY CANNOT PUT MORE THAN 19 CHARACTERS IN
              THE USERNAME FIELD DUE TO AN ATTRIBUTE IN THE
              <input> ELEMENT
        '''
        testUser = db.session.query(User) \
            .filter_by(email="automatedworkingemail@email.com").first()
        base_url = 'http://127.0.0.1:{}'.format(5000)
        self.open(base_url + "/profile/" + str(testUser.id))

        # SIGNING IN
        self.type("#email", "automatedworkingemail@email.com")
        self.type("#password", "testedPassword1!")
        self.click('#login-button')
        self.open(base_url + "/profile/" + str(testUser.id))
        
        self.click("#edit-profile-info")

        # Generate a random username
        choicesStr = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        usernameLen = random.randint(21, 32)
        rngUsername = ''  # The randomly-generated password
        for x in range(usernameLen):
            if x == usernameLen // 2:
                rngUsername += '2'
            val = random.randint(1, len(choicesStr))
            key = choicesStr[val - 1]
            rngUsername += key

        # Editing User Info
        self.type("#username", rngUsername)
        self.click("#submit-edits")
        self.scroll_to_bottom()
        self.save_screenshot('updateusername_toolongfail', 'test_screenshots')
        url = self.get_current_url()
        self.assert_true(url == (base_url + "/profile/" + str(testUser.id)))
        print("USERNAME HAS NOT CHANGED AS IT WAS INVALID")

    def test_userUpdateUsernamePass(self, *_):
        '''
        Test case of updating the user username where it works because
        the username passes the regex.
        '''
        testUser = db.session.query(User) \
            .filter_by(email="automatedworkingemail@email.com").first()
        base_url = 'http://127.0.0.1:{}'.format(5000)
        self.open(base_url + "/profile/" + str(testUser.id))

        # SIGNING IN
        self.type("#email", "automatedworkingemail@email.com")
        self.type("#password", "testedPassword1!")
        self.click('#login-button')
        self.open(base_url + "/profile/" + str(testUser.id))
        
        self.click("#edit-profile-info")

        # Generate a random username
        choicesStr = 'abcdefghijklmnopqrstuvwxyz'
        usernameLen = random.randint(8, 16)
        rngUsername = ''  # The randomly-generated password
        for x in range(usernameLen):
            if x == usernameLen // 2:
                rngUsername += "9"
            else:
                val = random.randint(1, len(choicesStr))
                if x == 6:
                    key = choicesStr[val - 1].upper()
                else:
                    key = choicesStr[val - 1]
                rngUsername += key

        # Editing User Info
        self.type("#username", rngUsername)
        self.click("#submit-edits")
        self.scroll_to_bottom()
        self.save_screenshot('updateusername_pass', 'test_screenshots')
        self.assert_text(rngUsername, "#username")
        print("USERNAME HAS CHANGED.")

    '''
    POSTAL CODE: uses Input Partition Testing

    Partitions:
        - Alphanumeric Only (fails: has a space)
        - Alphanumeric Only (passes: does not have a space)*
        - No Special Characters (fails: has a special char)
        - No Special Characters (passes: has no special chars)*
        - RegEx (fails: does not match A1A1A1 format)
        - RegEx (passes: matches A1A1A1 format)*
        *: Same test as the postal code can only be updated if it
           matches the regex and meets all criteria.
    '''

    def test_userUpdatePostalAlphaFail(self, *_):
        '''
        Test case where updating user postal code fails because
        postal code has a space in it.
        '''
        testUser = db.session.query(User) \
            .filter_by(email="automatedworkingemail@email.com").first()
        base_url = 'http://127.0.0.1:{}'.format(5000)
        self.open(base_url + "/profile/" + str(testUser.id))

        # SIGNING IN
        self.type("#email", "automatedworkingemail@email.com")
        self.type("#password", "testedPassword1!")
        self.click('#login-button')
        self.open(base_url + "/profile/" + str(testUser.id))
        
        self.click("#edit-profile-info")

        # Editing User Info
        self.type("#postalcode", "B1B 1B1")
        self.click("#submit-edits")
        self.save_screenshot('updatepost_alphafail', 'test_screenshots')
        url = self.get_current_url()
        self.assert_false(url == (base_url + "/profile/" + str(testUser.id)))
        print("ADDRESS HAS NOT CHANGED.")

    def test_userUpdatePostalSpecialFail(self, *_):
        '''
        Test case where updating user postal code fails because
        postal code has a special character in it.
        '''
        testUser = db.session.query(User) \
            .filter_by(email="automatedworkingemail@email.com").first()
        base_url = 'http://127.0.0.1:{}'.format(5000)
        self.open(base_url + "/profile/" + str(testUser.id))

        # SIGNING IN
        self.type("#email", "automatedworkingemail@email.com")
        self.type("#password", "testedPassword1!")
        self.click('#login-button')
        self.open(base_url + "/profile/" + str(testUser.id))
        
        self.click("#edit-profile-info")

        # Editing User Info
        self.type("#postalcode", "B1B!B1")
        self.click("#submit-edits")
        self.save_screenshot('updatepost_spcharfail', 'test_screenshots')
        url = self.get_current_url()
        self.assert_false(url == (base_url + "/profile/" + str(testUser.id)))
        print("ADDRESS HAS NOT CHANGED.")

    def test_userUpdatePostalLengthFail(self, *_):
        '''
        Test case where updating user postal code fails because
        postal code is too short.
        '''
        testUser = db.session.query(User) \
            .filter_by(email="automatedworkingemail@email.com").first()
        base_url = 'http://127.0.0.1:{}'.format(5000)
        self.open(base_url + "/profile/" + str(testUser.id))

        # SIGNING IN
        self.type("#email", "automatedworkingemail@email.com")
        self.type("#password", "testedPassword1!")
        self.click('#login-button')
        self.open(base_url + "/profile/" + str(testUser.id))
        
        self.click("#edit-profile-info")

        # Editing User Info
        self.type("#postalcode", "B1B")
        self.click("#submit-edits")
        self.save_screenshot('updatepost_lengthfail', 'test_screenshots')
        url = self.get_current_url()
        self.assert_false(url == (base_url + "/profile/" + str(testUser.id)))
        print("ADDRESS HAS NOT CHANGED.")

    def test_userUpdatePostalRegExFail(self, *_):
        '''
        Test case where updating user postal code fails because
        postal code does not match RegEx of a Canadian Postal Code.
        '''
        testUser = db.session.query(User) \
            .filter_by(email="automatedworkingemail@email.com").first()
        base_url = 'http://127.0.0.1:{}'.format(5000)
        self.open(base_url + "/profile/" + str(testUser.id))

        # SIGNING IN
        self.type("#email", "automatedworkingemail@email.com")
        self.type("#password", "testedPassword1!")
        self.click('#login-button')
        self.open(base_url + "/profile/" + str(testUser.id))
        
        self.click("#edit-profile-info")

        # Editing User Info
        self.type("#postalcode", "BBBB11")
        self.click("#submit-edits")
        self.save_screenshot('updatepost_regexfail', 'test_screenshots')
        url = self.get_current_url()
        self.assert_false(url == (base_url + "/profile/" + str(testUser.id)))
        print("ADDRESS HAS NOT CHANGED.")

    def test_userUpdatePostalRegExPass(self, *_):
        '''
        Test case where updating user postal code passes because
        postal code is of the right format, has no special chars.,
        and is alphanumeric only.
        '''
        testUser = db.session.query(User) \
            .filter_by(email="automatedworkingemail@email.com").first()
        base_url = 'http://127.0.0.1:{}'.format(5000)
        self.open(base_url + "/profile/" + str(testUser.id))

        # SIGNING IN
        self.type("#email", "automatedworkingemail@email.com")
        self.type("#password", "testedPassword1!")
        self.click('#login-button')
        self.open(base_url + "/profile/" + str(testUser.id))
        
        self.click("#edit-profile-info")

        # Editing User Info
        self.type("#postalcode", "B1B1B1")
        self.click("#submit-edits")
        self.scroll_to_bottom()
        self.save_screenshot('updatepost_pass', 'test_screenshots')
        self.assert_text("B1B1B1", "#postalcode")
        print("ADDRESS HAS CHANGED.")

    '''
    BILLING ADDRESS: Will not be tested as there are no given
    restrictions on what can be inputted as a billing address.
    '''
    