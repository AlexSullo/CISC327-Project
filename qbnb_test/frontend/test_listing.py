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
    date = str(datetime.datetime.now())[:10] + " to "
    date += "2022-02-12"
    testListingInfo = {"title": "Automated",
                       "owner": testUser.id,
                       "description": "Test description",
                       "price": float(10.01),
                       "booked": False,
                       "address": "1313 TestHouse dr.",
                       "dateAvailable": date,
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
        t = "Automated"
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
        # t = "Automated"
        # listing = db.session.query(Listing).filter_by(title=t).first()

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
        date = str(datetime.datetime.now())[:10]
        datesplit = date.split("-")
        datesplit[1] = int(datesplit[1]) + 3
        otherdate = datesplit.join("-")
        self.type("#dateAvailable", str(datetime.datetime.now())[:10])
        self.type("#dateAvailable", otherdate)
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

        self.type("#dateAvailable", "2022-12-11 to 2022-12-13")
        self.click("#submit-edits")

    # def test_coverImagePass(self, *_):
    #     '''
    #     Pass image if input correct file type.
    #     '''
    #     testUser = db.session.query(User) \
    #         .filter_by(email="automatedtestuser@email.com").first()
    #     base_url = 'http://127.0.0.1:{}'.format(5000)
    #     testListing = db.session.query(Listing) \
    #         .filter_by(title="Automated").first()
    #     self.open(base_url + "/profile/" + str(testUser.id))

    #     # SIGNING IN
    #     self.type("#email", "automatedtestuser@email.com")
    #     self.type("#password", "testedPassword1!")
    #     self.click('#login-button')
    #     self.open(base_url + "/listing/" + "/" + str(testListing.id))
    #     self.click("#edit")  # BlackBox testcity
    #     # t = "Automated"
    #     # listing = db.session.query(Listing).filter_by(title=t).first()
    #     im = open(os.path.join(sys.path[0], "test2.jpg"), "rb")
    #     data = im.read()
    #     render_pic = base64.b64encode(data).decode('ascii')

    #     self.input("#coverImage", render_pic)
    #     self.click("#submit-edits")

    # def test_coverImageFail(self, *_):
    #     '''
    #     Fail image if input incorrect file type.
    #     '''
    #     testUser = db.session.query(User) \
    #         .filter_by(email="automatedtestuser@email.com").first()
    #     base_url = 'http://127.0.0.1:{}'.format(5000)
    #     testListing = db.session.query(Listing) \
    #         .filter_by(title="Automated").first()
    #     self.open(base_url + "/profile/" + str(testUser.id))

    #     # SIGNING IN
    #     self.type("#email", "automatedtestuser@email.com")
    #     self.type("#password", "testedPassword1!")
    #     self.click('#login-button')
    #     self.open(base_url + "/listing/" + "/" + str(testListing.id))
    #     self.click("#edit")  # BlackBox testcity
    #     # t = "Automated"
    #     # listing = db.session.query(Listing).filter_by(title=t).first()
    #     # im = open(os.path.join(sys.path[0], "test2.jpg"),"rb")
    #     # data = im.read()
    #     # render_pic = base64.b64encode(data).decode('ascii')

    #     self.input("#coverImage", "test2.jpg")
    #     self.click("#submit-edits")

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
                print("Test Failed since attempted input")
                print("is less than current price")
            
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
    R5-4: Will not do a test for this since all 
    the requirements have been tested above
    '''

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
        length = random.randint(5, 20)
        title = " "
        for x in range(length):
            val = random.randint(1, len(choices))
            key = choices[val - 1]
            title += key
        # AUTOMATION
        # signing in
        testUser = db.session.query(User) \
            .filter_by(email="automatedtestuser@email.com").first()
        base_url = 'http://127.0.0.1:{}'.format(5000)
        self.open(base_url + "/profile/" + str(testUser.id))
        self.type("#email", "automatedtestuser@email.com")
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
        self.type("#dateAvailableStart", "2022")
        self.type("#dateAvailableStart", "1212")
        self.type("#dateAvailableEnd", "2023")
        self.type("#dateAvailableEnd", "0212")
        # submit form
        self.click("#create-listing")

    def test_R4_1_spaceMiddle_pass(self, *_):
        """
        Test case of inputting an alphanumeric title where it passes because 
        the title contains a space in the middle
        """
        # GENERATION
        choices = "abcdefghijklmnopqrstuvwxyz0123456789"
        length = random.randint(5, 20)
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
            .filter_by(email="automatedtestuser@email.com").first()
        self.open(base_url + "/profile/" + str(testUser.id))
        self.type("#email", "automatedtestuser@email.com")
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
        self.type("#dateAvailableStart", "2022")
        self.type("#dateAvailableStart", "1212")
        self.type("#dateAvailableEnd", "2023")
        self.type("#dateAvailableEnd", "0212")
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
            .filter_by(email="automatedtestuser@email.com").first()
        base_url = 'http://127.0.0.1:{}'.format(5000)
        self.open(base_url + "/profile/" + str(testUser.id))
        self.type("#email", "automatedtestuser@email.com")
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
        self.type("#dateAvailableStart", "2022")
        self.type("#dateAvailableStart", "1212")
        self.type("#dateAvailableEnd", "2023")
        self.type("#dateAvailableEnd", "0212")
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
            .filter_by(email="automatedtestuser@email.com").first()
        base_url = 'http://127.0.0.1:{}'.format(5000)
        self.open(base_url + "/profile/" + str(testUser.id))
        self.type("#email", "automatedtestuser@email.com")
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
        self.type("#dateAvailableStart", "2022")
        self.type("#dateAvailableStart", "1212")
        self.type("#dateAvailableEnd", "2023")
        self.type("#dateAvailableEnd", "0212")
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
            .filter_by(email="automatedtestuser@email.com").first()
        base_url = 'http://127.0.0.1:{}'.format(5000)
        self.open(base_url + "/profile/" + str(testUser.id))
        self.type("#email", "automatedtestuser@email.com")
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
        self.type("#dateAvailableStart", "2022")
        self.type("#dateAvailableStart", "1212")
        self.type("#dateAvailableEnd", "2023")
        self.type("#dateAvailableEnd", "0212")
        # submit form
        self.click("#create-listing")

    def test_R4_3_descriptionLessThan20_fail(self, *_):
        """
        Test case of inputting an arbitrary description where it fails because
        the length is less than 20 characters
        """
        # GENERATION
        choices = "abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(),./;:\'\""
        length = random.randint(13, 19)  # so description bigger than title
        description = ""
        for x in range(length):
            val = random.randint(1, len(choices))
            key = choices[val - 1]
            description += key
        # AUTOMATION
        # signing in
        testUser = db.session.query(User) \
            .filter_by(email="automatedtestuser@email.com").first()
        base_url = 'http://127.0.0.1:{}'.format(5000)
        self.open(base_url + "/profile/" + str(testUser.id))
        self.type("#email", "automatedtestuser@email.com")
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
        self.type("#dateAvailableStart", "2022")
        self.type("#dateAvailableStart", "1212")
        self.type("#dateAvailableEnd", "2023")
        self.type("#dateAvailableEnd", "0212")
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
            .filter_by(email="automatedtestuser@email.com").first()
        base_url = 'http://127.0.0.1:{}'.format(5000)
        self.open(base_url + "/profile/" + str(testUser.id))
        self.type("#email", "automatedtestuser@email.com")
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
        self.type("#dateAvailableStart", "2022")
        self.type("#dateAvailableStart", "1212")
        self.type("#dateAvailableEnd", "2023")
        self.type("#dateAvailableEnd", "0212")
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
            .filter_by(email="automatedtestuser@email.com").first()
        base_url = 'http://127.0.0.1:{}'.format(5000)
        self.open(base_url + "/profile/" + str(testUser.id))
        self.type("#email", "automatedtestuser@email.com")
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
        self.type("#dateAvailableStart", "2022")
        self.type("#dateAvailableStart", "1212")
        self.type("#dateAvailableEnd", "2023")
        self.type("#dateAvailableEnd", "0212")
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
            .filter_by(email="automatedtestuser@email.com").first()
        base_url = 'http://127.0.0.1:{}'.format(5000)
        self.open(base_url + "/profile/" + str(testUser.id))
        self.type("#email", "automatedtestuser@email.com")
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
        self.type("#dateAvailableStart", "2022")
        self.type("#dateAvailableStart", "1212")
        self.type("#dateAvailableEnd", "2023")
        self.type("#dateAvailableEnd", "0212")
        # submit form
        self.click("#create-listing")

    def test_R4_4_descriptionShorterThanTitle_fail(self, *_):
        """
        Test case of inputting an arbitrary description where it fails because
        the length is shorter than the length of the title
        """
        # GENERATION
        title = "this title has 28 characters"
        description = "this description fails"  # 22 characters
        # AUTOMATION
        # signing in
        testUser = db.session.query(User) \
            .filter_by(email="automatedtestuser@email.com").first()
        base_url = 'http://127.0.0.1:{}'.format(5000)
        self.open(base_url + "/profile/" + str(testUser.id))
        self.type("#email", "automatedtestuser@email.com")
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
        self.type("#dateAvailableStart", "2022")
        self.type("#dateAvailableStart", "1212")
        self.type("#dateAvailableEnd", "2023")
        self.type("#dateAvailableEnd", "0212")
        # submit form
        self.click("#create-listing")

    def test_R4_5_priceLessThan10_fail(self, *_):
        """
        Test case of inputting a price where it fails because it is less than 
        10
        """
        # GENERATION
        price = random.randint(0, 9)
        # AUTOMATION
        # signing in
        testUser = db.session.query(User) \
            .filter_by(email="automatedtestuser@email.com").first()
        base_url = 'http://127.0.0.1:{}'.format(5000)
        self.open(base_url + "/profile/" + str(testUser.id))
        self.type("#email", "automatedtestuser@email.com")
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
        self.type("#dateAvailableStart", "2022")
        self.type("#dateAvailableStart", "1212")
        self.type("#dateAvailableEnd", "2023")
        self.type("#dateAvailableEnd", "0212")
        # submit form
        self.click("#create-listing")

    def test_R4_5_priceBetween10And10000_pass(self, *_):
        """
        Test case of inputting a price where it passes because it is between
        10 and 10000
        """
        # GENERATION
        price = random.randint(10, 10000)
        # AUTOMATION
        # signing in
        testUser = db.session.query(User) \
            .filter_by(email="automatedtestuser@email.com").first()
        base_url = 'http://127.0.0.1:{}'.format(5000)
        self.open(base_url + "/profile/" + str(testUser.id))
        self.type("#email", "automatedtestuser@email.com")
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
        self.type("#dateAvailableStart", "2022")
        self.type("#dateAvailableStart", "1212")
        self.type("#dateAvailableEnd", "2023")
        self.type("#dateAvailableEnd", "0212")
        # submit form
        self.click("#create-listing")

    def test_R4_5_priceGreaterThan10000_fail(self, *_):
        """
        Test case of inputting a price where it fails because it is greater
        than 10000
        """
        # GENERATION
        price = random.randint(10001, 10002)
        # AUTOMATION
        # signing in
        testUser = db.session.query(User) \
            .filter_by(email="automatedtestuser@email.com").first()
        base_url = 'http://127.0.0.1:{}'.format(5000)
        self.open(base_url + "/profile/" + str(testUser.id))
        self.type("#email", "automatedtestuser@email.com")
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
        self.type("#dateAvailableStart", "2022")
        self.type("#dateAvailableStart", "1212")
        self.type("#dateAvailableEnd", "2023")
        self.type("#dateAvailableEnd", "0212")
        # submit form
        self.click("#create-listing")
