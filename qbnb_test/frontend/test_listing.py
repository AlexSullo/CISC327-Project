import random
from seleniumbase import BaseCase
from unittest.mock import patch
from qbnb.models import Listing, User, db

"""
This file defines all integration tests for listing creation
"""


class ListingCreationTest(BaseCase):

    # adds new test user to database
    testUserInfo = {"firstName": "Automated",
                    "surname": "Testuser",
                    "email": "automatedtestuser2@email.com",
                    "password": "testedPassword1!",
                    "billingAddress": "1212 Test Address",
                    "postalCode": "A1A1A1",
                    "username": "automateduser2"}
    
    testUser = User(testUserInfo)
    testUser.billingAddress = testUserInfo["billingAddress"]
    db.session.add(testUser)
    db.session.commit()

    '''
    Listing Creation Tests (Lucas Papadatos #20233257)
    title, description, and price.

    Specifications:
        - R4_1: Title is alphanumeric, space not allowed as prefix and suffix
        - R4_2: Title of the product is no longer than 80 characters
        - R4_3: Description length has to be of range [20,2000], arbitrary
        - R4_4: Description has to be longer than the product's title
        - R4_5: Price has to be of range [10, 10000]

    Uses 3 Blackbox Testing Methods:
        - Input Partition Testing (R4_2, R4_4)
        - Systematic Shotgun Testing (R4_1)
        - Boundary Testing (R4_3, R4_5)

    Input Partitions:
        - Title longer than 80 characters
        - Title shorter than 80 characters
        - Description longer than title
        - Description shorter than title

    Systematic Shotgun Partitions:
        - Randomly-generated with space as prefix 
        - Randomly-generated with space as suffix
        - Randomly-generated with space in middle

    Boundary Partitions:
        - Randomly-generated description less than 20 characters
        - Randomly-generated description between 20 and 2000 characters
        - Randomly-generated description greater than 2000 characters
        - Randomly-generated price less than 10
        - Randomly-generated price between 10 and 10000
        - Randomly-generated price greater than 10000

    Specification R4-6 cannot be tested as the lastModifiedDate is always set
    to the current time and therefore cannot fail the specification.

    Specification R4-7 cannot be tested because a user with an email must exist
    in order to create a listing.

    Specification R4-8 cannot be tested because names with the same title will
    have the same hashed id which cannot be true due to the unique constraint.
    '''

    def test_R4_1_spacePrefix_fail(self, *_):
        """
        Test case of inputting an alphanumeric title where it fails because the
        title contains a space at the prefix
        """
        # GENERATION
        choices = "abcdefghijklmnopqrstuvwxyz0123456789"
        length = random.randint(5,20)
        title = " "
        for x in range(length):
            val = random.randint(1, len(choices))
            key = choices[val - 1]
            title += key
        # AUTOMATION
        # signing in
        testUser = db.session.query(User) \
            .filter_by(email="automatedtestuser2@email.com").first()
        base_url = 'http://127.0.0.1:{}'.format(5000)
        self.open(base_url + "/profile/" + str(testUser.id))
        self.type("#email", "automatedtestuser2@email.com")
        self.type("#password", "testedPassword1!")
        self.click('#login-button')
        # open create page
        self.open(base_url + '/create')
        # enter title
        self.type("#title", title)
        # enter description
        self.type("#description", "I am pretty sure its a valid description.")
        # enter price
        self.type("#price", 999.99)
        # enter address
        self.type("#address", "123 Example Street")
        # enter location
        self.type("#location", "Kingston, ON")
        # enter building type
        self.type("#propertyType1", "House")
        # enter lot style
        self.type("#propertyType2", "Entire Lot")
        # enter num of bedrooms
        self.type("#propertyType3", 2)
        # enter num of bathrooms
        self.type("#propertyType4", 2)
        # enter date
        self.type("#dateAvailableStart","2022")
        self.type("#dateAvailableStart","1212")
        self.type("#dateAvailableEnd","2023")
        self.type("#dateAvailableEnd","0212")
        # submit form
        self.click("#create-listing")

    def test_R4_1_spaceMiddle_pass(self, *_):
        """
        Test case of inputting an alphanumeric title where it passes because 
        the title contains a space in the middle
        """
        # GENERATION
        choices = "abcdefghijklmnopqrstuvwxyz0123456789"
        length = random.randint(5,20)
        title = ""
        for x in range(length):
            val = random.randint(1, len(choices))
            key = choices[val - 1]
            title += key
        title += " "
        # AUTOMATION
        # signing in
        base_url = 'http://127.0.0.1:{}'.format(5000)
        testUser = db.session.query(User) \
            .filter_by(email="automatedtestuser2@email.com").first()
        self.open(base_url + "/profile/" + str(testUser.id))
        self.type("#email", "automatedtestuser2@email.com")
        self.type("#password", "testedPassword1!")
        self.click('#login-button')
        # open create page
        self.open(base_url + '/create')
        # enter title
        self.type("#title", title)
        # enter description
        self.type("#description", "I am pretty sure its a valid description.")
        # enter price
        self.type("#price", 999.99)
        # enter address
        self.type("#address", "123 Example Street")
        # enter location
        self.type("#location", "Kingston, ON")
        # enter building type
        self.type("#propertyType1", "House")
        # enter lot style
        self.type("#propertyType2", "Entire Lot")
        # enter num of bedrooms
        self.type("#propertyType3", 2)
        # enter num of bathrooms
        self.type("#propertyType4", 2)
        # enter date
        self.type("#dateAvailableStart","2022")
        self.type("#dateAvailableStart","1212")
        self.type("#dateAvailableEnd","2023")
        self.type("#dateAvailableEnd","0212")
        # submit form
        self.click("#create-listing")

    def test_R4_1_spaceSuffix_fail(self, *_):
        """
        Test case of inputting an alphanumeric title where it fails because the
        title contains a space at the suffix
        """
        # GENERATION
        choices = "abcdefghijklmnopqrstuvwxyz0123456789"
        length = 10
        title = ""
        for x in range(length):
            if (x == 5):
                title += " "
            val = random.randint(1, len(choices))
            key = choices[val - 1]
            title += key
        # AUTOMATION
        # signing in
        testUser = db.session.query(User) \
            .filter_by(email="automatedtestuser2@email.com").first()
        base_url = 'http://127.0.0.1:{}'.format(5000)
        self.open(base_url + "/profile/" + str(testUser.id))
        self.type("#email", "automatedtestuser2@email.com")
        self.type("#password", "testedPassword1!")
        self.click('#login-button')
        # open create page
        self.open(base_url + '/create')
        # enter title
        self.type("#title", title)
        # enter description
        self.type("#description", "I am pretty sure its a valid description.")
        # enter price
        self.type("#price", 999.99)
        # enter address
        self.type("#address", "123 Example Street")
        # enter location
        self.type("#location", "Kingston, ON")
        # enter building type
        self.type("#propertyType1", "House")
        # enter lot style
        self.type("#propertyType2", "Entire Lot")
        # enter num of bedrooms
        self.type("#propertyType3", 2)
        # enter num of bathrooms
        self.type("#propertyType4", 2)
        # enter date
        self.type("#dateAvailableStart","2022")
        self.type("#dateAvailableStart","1212")
        self.type("#dateAvailableEnd","2023")
        self.type("#dateAvailableEnd","0212")
        # submit form
        self.click("#create-listing")

    def test_R4_2_titleLongerThan80Chars_fail(self, *_):
        """
        Test case of inputting an alphanumeric title where it fails because the
        length is greater than 80 characters
        """
        # GENERATION
        title = "this is an invalid alphanumeric title for a qbnb listing \
        that is exactly 91 characters long"
        # AUTOMATION
        # signing in
        testUser = db.session.query(User) \
            .filter_by(email="automatedtestuser2@email.com").first()
        base_url = 'http://127.0.0.1:{}'.format(5000)
        self.open(base_url + "/profile/" + str(testUser.id))
        self.type("#email", "automatedtestuser2@email.com")
        self.type("#password", "testedPassword1!")
        self.click('#login-button')
        # open create page
        self.open(base_url + '/create')
        # enter title
        self.type("#title", title)
        # enter description
        self.type("#description", "I am pretty sure its a valid description.")
        # enter price
        self.type("#price", 999.99)
        # enter address
        self.type("#address", "123 Example Street")
        # enter location
        self.type("#location", "Kingston, ON")
        # enter building type
        self.type("#propertyType1", "House")
        # enter lot style
        self.type("#propertyType2", "Entire Lot")
        # enter num of bedrooms
        self.type("#propertyType3", 2)
        # enter num of bathrooms
        self.type("#propertyType4", 2)
        # enter date
        self.type("#dateAvailableStart","2022")
        self.type("#dateAvailableStart","1212")
        self.type("#dateAvailableEnd","2023")
        self.type("#dateAvailableEnd","0212")
        # submit form
        self.click("#create-listing")

    def test_R4_2_titleShorterThan80Chars_pass(self, *_):
        """
        Test case of inputting an alphanumeric title where it passes because
        the length is greater than 80 characters
        """
        # GENERATION
        title = "this is a valid alphanumeric title"
        # AUTOMATION
        # signing in
        testUser = db.session.query(User) \
            .filter_by(email="automatedtestuser2@email.com").first()
        base_url = 'http://127.0.0.1:{}'.format(5000)
        self.open(base_url + "/profile/" + str(testUser.id))
        self.type("#email", "automatedtestuser2@email.com")
        self.type("#password", "testedPassword1!")
        self.click('#login-button')
        # open create page
        self.open(base_url + '/create')
        # enter title
        self.type("#title", title)
        # enter description
        self.type("#description", "I'm pretty sure this a valid description.")
        # enter price
        self.type("#price", 999.99)
        # enter address
        self.type("#address", "123 Example Street")
        # enter location
        self.type("#location", "Kingston, ON")
        # enter building type
        self.type("#propertyType1", "House")
        # enter lot style
        self.type("#propertyType2", "Entire Lot")
        # enter num of bedrooms
        self.type("#propertyType3", 2)
        # enter num of bathrooms
        self.type("#propertyType4", 2)
        # enter date
        self.type("#dateAvailableStart","2022")
        self.type("#dateAvailableStart","1212")
        self.type("#dateAvailableEnd","2023")
        self.type("#dateAvailableEnd","0212")
        # submit form
        self.click("#create-listing")

    def test_R4_3_descriptionLessThan20_fail(self, *_):
        """
        Test case of inputting an arbitrary description where it fails because
        the length is less than 20 characters
        """
        # GENERATION
        choices = "abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(),./;:\'\""
        length = random.randint(13, 19) # so description bigger than title
        description = ""
        for x in range(length):
            val = random.randint(1, len(choices))
            key = choices[val - 1]
            description += key
        # AUTOMATION
        # signing in
        testUser = db.session.query(User) \
            .filter_by(email="automatedtestuser2@email.com").first()
        base_url = 'http://127.0.0.1:{}'.format(5000)
        self.open(base_url + "/profile/" + str(testUser.id))
        self.type("#email", "automatedtestuser2@email.com")
        self.type("#password", "testedPassword1!")
        self.click('#login-button')
        # open create page
        self.open(base_url + '/create')
        # enter title
        self.type("#title", "short title")
        # enter description
        self.type("#description", description)
        # enter price
        self.type("#price", 999.99)
        # enter address
        self.type("#address", "123 Example Street")
        # enter location
        self.type("#location", "Kingston, ON")
        # enter building type
        self.type("#propertyType1", "House")
        # enter lot style
        self.type("#propertyType2", "Entire Lot")
        # enter num of bedrooms
        self.type("#propertyType3", 2)
        # enter num of bathrooms
        self.type("#propertyType4", 2)
        # enter date
        self.type("#dateAvailableStart","2022")
        self.type("#dateAvailableStart","1212")
        self.type("#dateAvailableEnd","2023")
        self.type("#dateAvailableEnd","0212")
        # submit form
        self.click("#create-listing")

    def test_R4_3_descriptionBetween20And2000_pass(self, *_):
        """
        Test case of inputting an arbitrary description where it passes because
        the length is between 20 and 2000 characters
        """
        # GENERATION
        choices = "abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(),./;:\'\""
        length = random.randint(20, 2000)
        description = ""
        for x in range(length):
            val = random.randint(1, len(choices))
            key = choices[val - 1]
            description += key
        # AUTOMATION
        # signing in
        testUser = db.session.query(User) \
            .filter_by(email="automatedtestuser2@email.com").first()
        base_url = 'http://127.0.0.1:{}'.format(5000)
        self.open(base_url + "/profile/" + str(testUser.id))
        self.type("#email", "automatedtestuser2@email.com")
        self.type("#password", "testedPassword1!")
        self.click('#login-button')
        # open create page
        self.open(base_url + '/create')
        # enter title
        self.type("#title", "short title")
        # enter description
        self.type("#description", description)
        # enter price
        self.type("#price", 999.99)
        # enter address
        self.type("#address", "123 Example Street")
        # enter location
        self.type("#location", "Kingston, ON")
        # enter building type
        self.type("#propertyType1", "House")
        # enter lot style
        self.type("#propertyType2", "Entire Lot")
        # enter num of bedrooms
        self.type("#propertyType3", 2)
        # enter num of bathrooms
        self.type("#propertyType4", 2)
        # enter date
        self.type("#dateAvailableStart","2022")
        self.type("#dateAvailableStart","1212")
        self.type("#dateAvailableEnd","2023")
        self.type("#dateAvailableEnd","0212")
        # submit form
        self.click("#create-listing")

    def test_R4_3_descriptionGreaterThan2000_fail(self, *_):
        """
        Test case of inputting an arbitrary description where it fails because
        the length is greater than 2000 characters
        """
        # GENERATION
        choices = "abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(),./;:\'\""
        length = random.randint(2001, 2002)
        description = ""
        for x in range(length):
            val = random.randint(1, len(choices))
            key = choices[val - 1]
            description += key
        # AUTOMATION
        # signing in
        testUser = db.session.query(User) \
            .filter_by(email="automatedtestuser2@email.com").first()
        base_url = 'http://127.0.0.1:{}'.format(5000)
        self.open(base_url + "/profile/" + str(testUser.id))
        self.type("#email", "automatedtestuser2@email.com")
        self.type("#password", "testedPassword1!")
        self.click('#login-button')
        # open create page
        self.open(base_url + '/create')
        # enter title
        self.type("#title", "short title")
        # enter description
        self.type("#description", description)
        # enter price
        self.type("#price", 999.99)
        # enter address
        self.type("#address", "123 Example Street")
        # enter location
        self.type("#location", "Kingston, ON")
        # enter building type
        self.type("#propertyType1", "House")
        # enter lot style
        self.type("#propertyType2", "Entire Lot")
        # enter num of bedrooms
        self.type("#propertyType3", 2)
        # enter num of bathrooms
        self.type("#propertyType4", 2)
        # enter date
        self.type("#dateAvailableStart","2022")
        self.type("#dateAvailableStart","1212")
        self.type("#dateAvailableEnd","2023")
        self.type("#dateAvailableEnd","0212")
        # submit form
        self.click("#create-listing")

    def test_R4_4_descriptionLongerThanTitle_pass(self, *_):
        """
        Test case of inputting an arbitrary description where it passes because
        the length is longer than the length of the title
        """
        # GENERATION
        title = "this title has 28 characters"
        description = "this description passes with 42 characters"
        # AUTOMATION
        # signing in
        testUser = db.session.query(User) \
            .filter_by(email="automatedtestuser2@email.com").first()
        base_url = 'http://127.0.0.1:{}'.format(5000)
        self.open(base_url + "/profile/" + str(testUser.id))
        self.type("#email", "automatedtestuser2@email.com")
        self.type("#password", "testedPassword1!")
        self.click('#login-button')
        # open create page
        self.open(base_url + '/create')
        # enter title
        self.type("#title", title)
        # enter description
        self.type("#description", description)
        # enter price
        self.type("#price", 999.99)
        # enter address
        self.type("#address", "123 Example Street")
        # enter location
        self.type("#location", "Kingston, ON")
        # enter building type
        self.type("#propertyType1", "House")
        # enter lot style
        self.type("#propertyType2", "Entire Lot")
        # enter num of bedrooms
        self.type("#propertyType3", 2)
        # enter num of bathrooms
        self.type("#propertyType4", 2)
        # enter date
        self.type("#dateAvailableStart","2022")
        self.type("#dateAvailableStart","1212")
        self.type("#dateAvailableEnd","2023")
        self.type("#dateAvailableEnd","0212")
        # submit form
        self.click("#create-listing")

    def test_R4_4_descriptionShorterThanTitle_fail(self, *_):
        """
        Test case of inputting an arbitrary description where it fails because
        the length is shorter than the length of the title
        """
        # GENERATION
        title = "this title has 28 characters"
        description = "this description fails" # 22 characters
        # AUTOMATION
        # signing in
        testUser = db.session.query(User) \
            .filter_by(email="automatedtestuser2@email.com").first()
        base_url = 'http://127.0.0.1:{}'.format(5000)
        self.open(base_url + "/profile/" + str(testUser.id))
        self.type("#email", "automatedtestuser2@email.com")
        self.type("#password", "testedPassword1!")
        self.click('#login-button')
        # open create page
        self.open(base_url + '/create')
        # enter title
        self.type("#title", title)
        # enter description
        self.type("#description", description)
        # enter price
        self.type("#price", 999.99)
        # enter address
        self.type("#address", "123 Example Street")
        # enter location
        self.type("#location", "Kingston, ON")
        # enter building type
        self.type("#propertyType1", "House")
        # enter lot style
        self.type("#propertyType2", "Entire Lot")
        # enter num of bedrooms
        self.type("#propertyType3", 2)
        # enter num of bathrooms
        self.type("#propertyType4", 2)
        # enter date
        self.type("#dateAvailableStart","2022")
        self.type("#dateAvailableStart","1212")
        self.type("#dateAvailableEnd","2023")
        self.type("#dateAvailableEnd","0212")
        # submit form
        self.click("#create-listing")

    def test_R4_5_priceLessThan10_fail(self, *_):
        """
        Test case of inputting a price where it fails because it is less than 
        10
        """
        # GENERATION
        price = random.randint(0,9)
        # AUTOMATION
        # signing in
        testUser = db.session.query(User) \
            .filter_by(email="automatedtestuser2@email.com").first()
        base_url = 'http://127.0.0.1:{}'.format(5000)
        self.open(base_url + "/profile/" + str(testUser.id))
        self.type("#email", "automatedtestuser2@email.com")
        self.type("#password", "testedPassword1!")
        self.click('#login-button')
        # open create page
        self.open(base_url + '/create')
        # enter title
        self.type("#title", "valid title")
        # enter description
        self.type("#description", "I'm pre sure this is a valid description")
        # enter price
        self.type("#price", price)
        # enter address
        self.type("#address", "123 Example Street")
        # enter location
        self.type("#location", "Kingston, ON")
        # enter building type
        self.type("#propertyType1", "House")
        # enter lot style
        self.type("#propertyType2", "Entire Lot")
        # enter num of bedrooms
        self.type("#propertyType3", 2)
        # enter num of bathrooms
        self.type("#propertyType4", 2)
        # enter date
        self.type("#dateAvailableStart","2022")
        self.type("#dateAvailableStart","1212")
        self.type("#dateAvailableEnd","2023")
        self.type("#dateAvailableEnd","0212")
        # submit form
        self.click("#create-listing")

    def test_R4_5_priceBetween10And10000_pass(self, *_):
        """
        Test case of inputting a price where it passes because it is between
        10 and 10000
        """
        # GENERATION
        price = random.randint(10,10000)
        # AUTOMATION
        # signing in
        testUser = db.session.query(User) \
            .filter_by(email="automatedtestuser2@email.com").first()
        base_url = 'http://127.0.0.1:{}'.format(5000)
        self.open(base_url + "/profile/" + str(testUser.id))
        self.type("#email", "automatedtestuser2@email.com")
        self.type("#password", "testedPassword1!")
        self.click('#login-button')
        # open create page
        self.open(base_url + '/create')
        # enter title
        self.type("#title", "valid title")
        # enter description
        self.type("#description", "I'm pre sure this is a valid description")
        # enter price
        self.type("#price", price)
        # enter address
        self.type("#address", "123 Example Street")
        # enter location
        self.type("#location", "Kingston, ON")
        # enter building type
        self.type("#propertyType1", "House")
        # enter lot style
        self.type("#propertyType2", "Entire Lot")
        # enter num of bedrooms
        self.type("#propertyType3", 2)
        # enter num of bathrooms
        self.type("#propertyType4", 2)
        # enter date
        self.type("#dateAvailableStart","2022")
        self.type("#dateAvailableStart","1212")
        self.type("#dateAvailableEnd","2023")
        self.type("#dateAvailableEnd","0212")
        # submit form
        self.click("#create-listing")

    def test_R4_5_priceGreaterThan10000_fail(self, *_):
        """
        Test case of inputting a price where it fails because it is greater
        than 10000
        """
        # GENERATION
        price = random.randint(10001,10002)
        # AUTOMATION
        # signing in
        testUser = db.session.query(User) \
            .filter_by(email="automatedtestuser2@email.com").first()
        base_url = 'http://127.0.0.1:{}'.format(5000)
        self.open(base_url + "/profile/" + str(testUser.id))
        self.type("#email", "automatedtestuser2@email.com")
        self.type("#password", "testedPassword1!")
        self.click('#login-button')
        # open create page
        self.open(base_url + '/create')
        # enter title
        self.type("#title", "valid title")
        # enter description
        self.type("#description", "I'm pre sure this is a valid description")
        # enter price
        self.type("#price", price)
        # enter address
        self.type("#address", "123 Example Street")
        # enter location
        self.type("#location", "Kingston, ON")
        # enter building type
        self.type("#propertyType1", "House")
        # enter lot style
        self.type("#propertyType2", "Entire Lot")
        # enter num of bedrooms
        self.type("#propertyType3", 2)
        # enter num of bathrooms
        self.type("#propertyType4", 2)
        # enter date
        self.type("#dateAvailableStart","2022")
        self.type("#dateAvailableStart","1212")
        self.type("#dateAvailableEnd","2023")
        self.type("#dateAvailableEnd","0212")
        # submit form
        self.click("#create-listing")