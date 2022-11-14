from seleniumbase import BaseCase
from unittest.mock import patch
from qbnb.models import Listing, User, db
from flask import Flask, redirect, render_template, jsonify, request
import random
from random import uniform
import datetime
from curses.ascii import isalnum
import base64
import os
import sys
# from PIL import Image


class updateListingPageTest(BaseCase):
    # python -m pytest qbnb_test\frontend
    # don't have to run from qbnb
    # python -m flask --app __main__ --debug run  
    # cd qbnb
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
    testUser = db.session.query(User) \
        .filter_by(email="automatedtestuser@email.com").first()  
    im = open(os.path.join(sys.path[0], "test.jpg"), "rb")
    data = im.read()
    render_pic = base64.b64encode(data).decode('ascii')
    testListingInfo = {"title": "Automated",
                       "owner": testUser.id,
                       "description": "Test description",
                       "price": float(10.01),
                       "booked": False,
                       "address": "1313 TestHouse dr.",
                       "dateAvailable": datetime.datetime.now(),
                       "imgData": data,
                       "imgRenderedData": render_pic,
                       "propertyType1": "House",
                       "propertyType2": "apartment",
                       "propertyType3": "room",
                       "propertyType4": "bathroom",
                       "location": "1234 Kingston Ave"}
    # "imgRenderedData" : "",
    testListing = Listing(testListingInfo)
    # testListing.imgRenderedData = testListing['imgRenderedData']
    db.session.add(testListing)
    db.session.commit()
    print(testListing.id)

    '''
    R5-1
    Blackbox testing type: Input partitioning
    '''
    def test_UpdateTitlePass(self, *_):
        # make more functions
        testUser = db.session.query(User) \
            .filter_by(email="automatedtestuser@email.com").first()
        base_url = 'http://127.0.0.1:{}'.format(5000)
        testListing = db.session.query(Listing) \
            .filter_by(title="Automated").first()
        self.open(base_url + "/profile/" + str(testUser.id))

        # SIGNING IN
        self.type("#email", "automatedtestuser@email.com")
        self.type("#password", "testedPassword1!")
        self.click('#login-button')
        self.open(base_url + "/listing/" + "/" + str(testListing.id))
        self.click("#edit")  # BlackBox testcity

        # Updating Title
        self.type("#title", "New Title")
        self.click("#submit-edits")

    def test_UpdateTitleFail(self, *_):
        # make more functions
        testUser = db.session.query(User) \
            .filter_by(email="automatedtestuser@email.com").first()
        base_url = 'http://127.0.0.1:{}'.format(5000)
        testListing = db.session.query(Listing) \
            .filter_by(title="Automated").first()
        self.open(base_url + "/profile/" + str(testUser.id))

        # SIGNING IN
        self.type("#email", "automatedtestuser@email.com")
        self.type("#password", "testedPassword1!")
        self.click('#login-button')
        self.open(base_url + "/listing/" + "/" + str(testListing.id))
        self.click("#edit")  # BlackBox testcity

        # Updating Title
        self.type("#title", "!!!!NOtWork!!!")
        self.click("#submit-edits")

    def test_description(self, *_):
        '''
        Will only have one test for description since it will always pass,
        regardless of characters in use and if it is empty.
        '''
        # make more functions
        testUser = db.session.query(User) \
            .filter_by(email="automatedtestuser@email.com").first()
        base_url = 'http://127.0.0.1:{}'.format(5000)
        testListing = db.session.query(Listing) \
            .filter_by(title="Automated").first()
        self.open(base_url + "/profile/" + str(testUser.id))

        # SIGNING IN
        self.type("#email", "automatedtestuser@email.com")
        self.type("#password", "testedPassword1!")
        self.click('#login-button')
        self.open(base_url + "/listing/" + "/" + str(testListing.id))
        self.click("#edit")  # BlackBox testcity

        # Updating Description
        self.type("#description", "Hello this is a test description")
        self.click("#submit-edits")

    def test_pricePass(self, *_):
        # make more functions
        testUser = db.session.query(User) \
            .filter_by(email="automatedtestuser@email.com").first()
        base_url = 'http://127.0.0.1:{}'.format(5000)
        testListing = db.session.query(Listing) \
            .filter_by(title="Automated").first()
        self.open(base_url + "/profile/" + str(testUser.id))

        # SIGNING IN
        self.type("#email", "automatedtestuser@email.com")
        self.type("#password", "testedPassword1!")
        self.click('#login-button')
        self.open(base_url + "/listing/" + "/" + str(testListing.id))
        self.click("#edit")  # BlackBox testcity
        t="Automated"
        listing = db.session.query(Listing).filter_by(title=t).first()
        currentListingPrice = float(listing.price) + 0.01

        # Updating Price
        self.type("#price", currentListingPrice)
        self.click("#submit-edits")
    
    def test_priceFail(self, *_):
        # make more functions
        testUser = db.session.query(User) \
            .filter_by(email="automatedtestuser@email.com").first()
        base_url = 'http://127.0.0.1:{}'.format(5000)
        testListing = db.session.query(Listing) \
            .filter_by(title="Automated").first()
        self.open(base_url + "/profile/" + str(testUser.id))

        # SIGNING IN
        self.type("#email", "automatedtestuser@email.com")
        self.type("#password", "testedPassword1!")
        self.click('#login-button')
        self.open(base_url + "/listing/" + "/" + str(testListing.id))
        self.click("#edit")  # BlackBox testcity
        t = "Automated"
        listing = db.session.query(Listing).filter_by(title=t).first()
        currentListingPrice = float(listing.price) - 0.01

        # Updating Price
        self.type("#price", currentListingPrice)
        self.click("#submit-edits")

    def test_booked(self, *_):
        '''
        Will have only one test for the booked option since the
        checkbox can only be checked/unchecked and no other action.
        '''
        testUser = db.session.query(User) \
            .filter_by(email="automatedtestuser@email.com").first()
        base_url = 'http://127.0.0.1:{}'.format(5000)
        testListing = db.session.query(Listing) \
            .filter_by(title="Automated").first()
        self.open(base_url + "/profile/" + str(testUser.id))

        # SIGNING IN
        self.type("#email", "automatedtestuser@email.com")
        self.type("#password", "testedPassword1!")
        self.click('#login-button')
        self.open(base_url + "/listing/" + "/" + str(testListing.id))
        self.click("#edit")  # BlackBox testcity
        # listing = db.session.query(Listing).filter_by(title="Automated").first()

        self.check_if_unchecked("#booked")
        self.click("#submit-edits")

    def test_addressCreatePass(self, *_):
        '''
        Pass address if it meets the regex.
        '''
        testUser = db.session.query(User) \
            .filter_by(email="automatedtestuser@email.com").first()
        base_url = 'http://127.0.0.1:{}'.format(5000)
        testListing = db.session.query(Listing) \
            .filter_by(title="Automated").first()
        self.open(base_url + "/profile/" + str(testUser.id))

        # SIGNING IN
        self.type("#email", "automatedtestuser@email.com")
        self.type("#password", "testedPassword1!")
        self.click('#login-button')
        self.open(base_url + "/listing/" + "/" + str(testListing.id))
        self.click("#edit")  # BlackBox testcity
        # t = "Automated"
        # listing = db.session.query(Listing).filter_by(title=t).first()

        self.type("#address", "1234 Testcity rd.")
        self.click("#submit-edits")

    def test_addressCreateFail(self, *_):
        '''
        Fail address if it not meets the regex.
        '''
        testUser = db.session.query(User) \
            .filter_by(email="automatedtestuser@email.com").first()
        base_url = 'http://127.0.0.1:{}'.format(5000)
        testListing = db.session.query(Listing) \
            .filter_by(title="Automated").first()
        self.open(base_url + "/profile/" + str(testUser.id))

        # SIGNING IN
        self.type("#email", "automatedtestuser@email.com")
        self.type("#password", "testedPassword1!")
        self.click('#login-button')
        self.open(base_url + "/listing/" + "/" + str(testListing.id))
        self.click("#edit")  # BlackBox testcity
        # t = "Automated"
        # listing = db.session.query(Listing).filter_by(title=t).first()

        self.type("#address", "rd. Test 1234")
        self.click("#submit-edits")

    def test_dateAvailablePass(self, *_):
        '''
        Pass date available if it meets the datetime format.
        '''
        testUser = db.session.query(User) \
            .filter_by(email="automatedtestuser@email.com").first()
        base_url = 'http://127.0.0.1:{}'.format(5000)
        testListing = db.session.query(Listing) \
            .filter_by(title="Automated").first()
        self.open(base_url + "/profile/" + str(testUser.id))

        # SIGNING IN
        self.type("#email", "automatedtestuser@email.com")
        self.type("#password", "testedPassword1!")
        self.click('#login-button')
        self.open(base_url + "/listing/" + "/" + str(testListing.id))
        self.click("#edit")  # BlackBox testcity
        # t = "Automated"
        # listing = db.session.query(Listing).filter_by(title=t).first()

        self.type("#dateAvailable", datetime.datetime.now())
        self.click("#submit-edits")

    def test_dateAvailableFail(self, *_):
        '''
        Pass date available if it meets the datetime format.
        '''
        testUser = db.session.query(User) \
            .filter_by(email="automatedtestuser@email.com").first()
        base_url = 'http://127.0.0.1:{}'.format(5000)
        testListing = db.session.query(Listing) \
            .filter_by(title="Automated").first()
        self.open(base_url + "/profile/" + str(testUser.id))

        # SIGNING IN
        self.type("#email", "automatedtestuser@email.com")
        self.type("#password", "testedPassword1!")
        self.click('#login-button')
        self.open(base_url + "/listing/" + "/" + str(testListing.id))
        self.click("#edit")  # BlackBox testcity
        # t = "Automated"
        # listing = db.session.query(Listing).filter_by(title=t).first()

        self.type("#dateAvailable", "November 13th, 2022")
        self.click("#submit-edits")

    def test_coverImagePass(self, *_):
        '''
        Pass image if input correct file type.
        '''
        testUser = db.session.query(User) \
            .filter_by(email="automatedtestuser@email.com").first()
        base_url = 'http://127.0.0.1:{}'.format(5000)
        testListing = db.session.query(Listing) \
            .filter_by(title="Automated").first()
        self.open(base_url + "/profile/" + str(testUser.id))

        # SIGNING IN
        self.type("#email", "automatedtestuser@email.com")
        self.type("#password", "testedPassword1!")
        self.click('#login-button')
        self.open(base_url + "/listing/" + "/" + str(testListing.id))
        self.click("#edit")  # BlackBox testcity
        # t = "Automated"
        # listing = db.session.query(Listing).filter_by(title=t).first()
        im = open(os.path.join(sys.path[0], "test2.jpg"), "rb")
        data = im.read()
        render_pic = base64.b64encode(data).decode('ascii')

        self.input("#coverImage", render_pic)
        self.click("#submit-edits")

    def test_coverImageFail(self, *_):
        '''
        Fail image if input incorrect file type.
        '''
        testUser = db.session.query(User) \
            .filter_by(email="automatedtestuser@email.com").first()
        base_url = 'http://127.0.0.1:{}'.format(5000)
        testListing = db.session.query(Listing) \
            .filter_by(title="Automated").first()
        self.open(base_url + "/profile/" + str(testUser.id))

        # SIGNING IN
        self.type("#email", "automatedtestuser@email.com")
        self.type("#password", "testedPassword1!")
        self.click('#login-button')
        self.open(base_url + "/listing/" + "/" + str(testListing.id))
        self.click("#edit")  # BlackBox testcity
        # t = "Automated"
        # listing = db.session.query(Listing).filter_by(title=t).first()
        # im = open(os.path.join(sys.path[0], "test2.jpg"),"rb")
        # data = im.read()
        # render_pic = base64.b64encode(data).decode('ascii')

        self.input("#coverImage", "test2.jpg")
        self.click("#submit-edits")

    def test_propertyType1Pass(self, *_):
        '''
        Fail propertytype1 if input correct regex.
        '''
        testUser = db.session.query(User) \
            .filter_by(email="automatedtestuser@email.com").first()
        base_url = 'http://127.0.0.1:{}'.format(5000)
        testListing = db.session.query(Listing) \
            .filter_by(title="Automated").first()
        self.open(base_url + "/profile/" + str(testUser.id))

        # SIGNING IN
        self.type("#email", "automatedtestuser@email.com")
        self.type("#password", "testedPassword1!")
        self.click('#login-button')
        self.open(base_url + "/listing/" + "/" + str(testListing.id))
        self.click("#edit")  # BlackBox testcity
        # t = "Automated"
        # listing = db.session.query(Listing).filter_by(title=t).first()

        self.input("#propertyType1", "House")
        self.click("#submit-edits")
    
    def test_propertyType1Fail(self, *_):
        '''
        Fail propertytype1 if input incorrect regex.
        '''
        testUser = db.session.query(User) \
            .filter_by(email="automatedtestuser@email.com").first()
        base_url = 'http://127.0.0.1:{}'.format(5000)
        testListing = db.session.query(Listing) \
            .filter_by(title="Automated").first()
        self.open(base_url + "/profile/" + str(testUser.id))

        # SIGNING IN
        self.type("#email", "automatedtestuser@email.com")
        self.type("#password", "testedPassword1!")
        self.click('#login-button')
        self.open(base_url + "/listing/" + "/" + str(testListing.id))
        self.click("#edit")  # BlackBox testcity
        # t = "Automated"
        # listing = db.session.query(Listing).filter_by(title=t).first()

        self.input("#propertyType1", "!!!!!house!!!!")
        self.click("#submit-edits")

    def test_propertyType2Pass(self, *_):
        '''
        Pass propertytype2 if input correct regex.
        '''
        testUser = db.session.query(User) \
            .filter_by(email="automatedtestuser@email.com").first()
        base_url = 'http://127.0.0.1:{}'.format(5000)
        testListing = db.session.query(Listing) \
            .filter_by(title="Automated").first()
        self.open(base_url + "/profile/" + str(testUser.id))

        # SIGNING IN
        self.type("#email", "automatedtestuser@email.com")
        self.type("#password", "testedPassword1!")
        self.click('#login-button')
        self.open(base_url + "/listing/" + "/" + str(testListing.id))
        self.click("#edit")  # BlackBox testcity
        # t = "Automated"
        # listing = db.session.query(Listing).filter_by(title=t).first()

        self.type("#propertyType2", "apartment")
        self.click("#submit-edits")
    
    def test_propertyType2Fail(self, *_):
        '''
        Fail propertytype2 if input incorrect regex.
        '''
        testUser = db.session.query(User) \
            .filter_by(email="automatedtestuser@email.com").first()
        base_url = 'http://127.0.0.1:{}'.format(5000)
        testListing = db.session.query(Listing) \
            .filter_by(title="Automated").first()
        self.open(base_url + "/profile/" + str(testUser.id))

        # SIGNING IN
        self.type("#email", "automatedtestuser@email.com")
        self.type("#password", "testedPassword1!")
        self.click('#login-button')
        self.open(base_url + "/listing/" + "/" + str(testListing.id))
        self.click("#edit")  # BlackBox testcity
        # t = "Automated"
        # listing = db.session.query(Listing).filter_by(title=t).first()

        self.type("#propertyType2", "!!!!@@@####apartment")
        self.click("#submit-edits")

    def test_propertyType3Pass(self, *_):
        '''
        Pass propertytype3 if input correct regex.
        '''
        testUser = db.session.query(User) \
            .filter_by(email="automatedtestuser@email.com").first()
        base_url = 'http://127.0.0.1:{}'.format(5000)
        testListing = db.session.query(Listing) \
            .filter_by(title="Automated").first()
        self.open(base_url + "/profile/" + str(testUser.id))

        # SIGNING IN
        self.type("#email", "automatedtestuser@email.com")
        self.type("#password", "testedPassword1!")
        self.click('#login-button')
        self.open(base_url + "/listing/" + "/" + str(testListing.id))
        self.click("#edit")  # BlackBox testcity
        # t = "Automated"
        # listing = db.session.query(Listing).filter_by(title=t).first()

        self.input("#propertyType3", "one room")
        self.click("#submit-edits")
    
    def test_propertyType3Fail(self, *_):
        '''
        Fail propertytype3 if input incorrect regex.
        '''
        testUser = db.session.query(User) \
            .filter_by(email="automatedtestuser@email.com").first()
        base_url = 'http://127.0.0.1:{}'.format(5000)
        testListing = db.session.query(Listing) \
            .filter_by(title="Automated").first()
        self.open(base_url + "/profile/" + str(testUser.id))

        # SIGNING IN
        self.type("#email", "automatedtestuser@email.com")
        self.type("#password", "testedPassword1!")
        self.click('#login-button')
        self.open(base_url + "/listing/" + "/" + str(testListing.id))
        self.click("#edit")  # BlackBox testcity
        # t = "Automated"
        # listing = db.session.query(Listing).filter_by(title=t).first()

        self.type("#propertyType3", "!!!!~`````one room")
        self.click("#submit-edits")

    def test_propertyType4Pass(self, *_):
        '''
        Pass propertytype4 if input correct regex.
        '''
        testUser = db.session.query(User) \
            .filter_by(email="automatedtestuser@email.com").first()
        base_url = 'http://127.0.0.1:{}'.format(5000)
        testListing = db.session.query(Listing) \
            .filter_by(title="Automated").first()
        self.open(base_url + "/profile/" + str(testUser.id))

        # SIGNING IN
        self.type("#email", "automatedtestuser@email.com")
        self.type("#password", "testedPassword1!")
        self.click('#login-button')
        self.open(base_url + "/listing/" + "/" + str(testListing.id))
        self.click("#edit")  # BlackBox testcity
        # t = "Automated"
        # listing = db.session.query(Listing).filter_by(title=t).first()

        self.type("#propertyType4", "bathroom")
        self.click("#submit-edits")

    def test_propertyType4Fail(self, *_):
        '''
        Fail propertytype4 if input incorrect regex.
        '''
        testUser = db.session.query(User) \
            .filter_by(email="automatedtestuser@email.com").first()
        base_url = 'http://127.0.0.1:{}'.format(5000)
        testListing = db.session.query(Listing) \
            .filter_by(title="Automated").first()
        self.open(base_url + "/profile/" + str(testUser.id))

        # SIGNING IN
        self.type("#email", "automatedtestuser@email.com")
        self.type("#password", "testedPassword1!")
        self.click('#login-button')
        self.open(base_url + "/listing/" + "/" + str(testListing.id))
        self.click("#edit")  # BlackBox testcity
        # t = "Automated"
        # listing = db.session.query(Listing).filter_by(title=t).first()

        self.type("#propertyType4", "(**(&^&*^%*^%&one bathroom")
        self.click("#submit-edits")
    
    def test_locationPass(self, *_):
        '''
        Pass location if input correct regex.
        '''
        testUser = db.session.query(User) \
            .filter_by(email="automatedtestuser@email.com").first()
        base_url = 'http://127.0.0.1:{}'.format(5000)
        testListing = db.session.query(Listing) \
            .filter_by(title="Automated").first()
        self.open(base_url + "/profile/" + str(testUser.id))

        # SIGNING IN
        self.type("#email", "automatedtestuser@email.com")
        self.type("#password", "testedPassword1!")
        self.click('#login-button')
        self.open(base_url + "/listing/" + "/" + str(testListing.id))
        self.click("#edit")  # BlackBox testcity
        # t = "Automated"
        # listing = db.session.query(Listing).filter_by(title=t).first()

        self.type("#location", "1234 kingston rd")
        self.click("#submit-edits")

    def test_locationFail(self, *_):
        '''
        Fail location if input incorrect regex.
        '''
        testUser = db.session.query(User) \
            .filter_by(email="automatedtestuser@email.com").first()
        base_url = 'http://127.0.0.1:{}'.format(5000)
        testListing = db.session.query(Listing) \
            .filter_by(title="Automated").first()
        self.open(base_url + "/profile/" + str(testUser.id))

        # SIGNING IN
        self.type("#email", "automatedtestuser@email.com")
        self.type("#password", "testedPassword1!")
        self.click('#login-button')
        self.open(base_url + "/listing/" + "/" + str(testListing.id))
        self.click("#edit")  # BlackBox testcity
        # t = "Automated"
        # listing = db.session.query(Listing).filter_by(title=t).first()

        self.type("#location", "Road of kingston 1234")
        self.click("#submit-edits")

    """
    R5-2
    Blackbox testing type: Shotgun testing for the price values
    """
    def test_PriceOnlyIncreased(self, *_):
        """
        R5-2, Tests that price can only be increased. 
        Additionally that stays in range of $10 and $10000.
        Will be using shotgun BlackBox testing for this
        """
        testUser = db.session.query(User) \
            .filter_by(email="automatedtestuser@email.com").first()
        base_url = 'http://127.0.0.1:{}'.format(5000)
        testListing = db.session.query(Listing) \
            .filter_by(title="Automated").first()
        self.open(base_url + "/profile/" + str(testUser.id))

        # SIGNING IN
        self.type("#email", "automatedtestuser@email.com")
        self.type("#password", "testedPassword1!")
        self.click('#login-button')
        self.open(base_url + "/listing/" + "/" + str(testListing.id))
        self.click("#edit")  # BlackBox testcity
        r = 10
        testList = []
        
        for i in range(0, r):
            n = round(uniform(10, 10000), 2)
            testList.append(n)
        print(testList)
        t = "Automated"
        listing = db.session.query(Listing).filter_by(title=t).first()
        currentListingPrice = float(listing.price)
        print(currentListingPrice)

        for i in testList:

            if i > currentListingPrice and i < 10000:
                self.type("#price", float(i))
                self.click("#submit-edits")
                print("TestPrice", i)
                print("Test Passed since in bounds")
                print("and greater than current price")
            
            elif i < currentListingPrice and i > 10:
                self.type("#price", float(i))
                self.click("#submit-edits")
                print("TestPrice", i)
                print("Test Failed since attempted input is less than current price")
            
            elif i < 10:
                self.type("#price", float(i))
                self.click("#submit-edits")
                print("TestPrice", i)
                print("Test Failed since attempted input out of bounds")
            
            elif i > 10000:
                self.type("#price", float(i))
                self.click("#submit-edits")
                print("TestPrice", i)
                print("Test Failed since attempted input out of bounds")

    """
    R5-3
    Blackbox Testing type: output coverage
    """
    def test_lastModifiedDatePass(self, *_):
        '''
        Output coverage pass if datetime == now(),
        else test fails. Checking output.
        '''
        testUser = db.session.query(User) \
            .filter_by(email="automatedtestuser@email.com").first()
        base_url = 'http://127.0.0.1:{}'.format(5000)
        testListing = db.session.query(Listing) \
            .filter_by(title="Automated").first()
        self.open(base_url + "/profile/" + str(testUser.id))

        # SIGNING IN
        self.type("#email", "automatedtestuser@email.com")
        self.type("#password", "testedPassword1!")
        self.click('#login-button')
        self.open(base_url + "/listing/" + "/" + str(testListing.id))
        self.click("#edit")  # BlackBox testcity
        # t = "Automated"
        # listing = db.session.query(Listing).filter_by(title=t).first()

        self.click("#submit-edits")

        if testListing.lastModifiedDate == datetime.datetime.now():
            print("The datetime should be equal to now so test pass")
        else:
            print("if lastmodifieddate not equal to now() test failed")
    
    '''
    R5-4: Will not do a test for this since all the requirements have been tested above
    '''
