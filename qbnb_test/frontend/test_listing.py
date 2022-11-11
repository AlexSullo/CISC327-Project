from seleniumbase import BaseCase
from unittest.mock import patch
from qbnb.models import Listing, User,db
import random
from random import uniform
import datetime

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

    testListingInfo = {"title": "Automated",
                       "owner": testUser.id,
                       "description": "Test description",
                       "price": "10.01",
                       "booked": "False",
                       "address": "1313 TestHouse dr.",
                       "dateAvailable": "2022-11-29 13:20:11.558674",
                       "imgData": "",
                       "coverImage": "image.png",
                       "propertyType1": "House",
                       "propertyType2": "apartment",
                       "propertyType3": "room",
                       "propertyType4": "bathroom",
                       "location": "1234 Kingston Ave"}

    testListing = Listing(testListingInfo)
    # testListing.owner = testUser.id
    db.session.add(testListing)
    db.session.commit()

    

    # def test_UpdateAllAtributes(self, *_):
    #     """
    #     R5-1, Tests that all atributes can be updated except for owner_id
    #     and last_modified_date
    #     """
    #     #make more functions

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
        self.open(base_url +  "/updatelisting" + "/" + testListing.id + "/")
        self.click("#edit") #BlackBox testcity
        r = 10
        testList = []
        
        for i in range(0,r):
            n = round(uniform(10,10000),2)
            testList.append(n)
        print(testList)
        listing = db.session.query(Listing).filter_by(id=-5944238697326520506).first()
        currentListingPrice = float(listing.price)
        print(currentListingPrice)

        for i in testList:
            
            if i > currentListingPrice and i < 10000:
                self.type("#price", float(i))
                self.click("#submit-edits")
                print("TestPrice",i)
                print("Test Passed since in bounds and greater than current price")
            
            elif i < currentListingPrice and i > 10:
                self.type("#price", float(i))
                self.click("#submit-edits")
                print("TestPrice",i)
                print("Test Failed since attempted input is less than current price")
            
            elif i < 10:
                self.type("#price", float(i))
                self.click("#submit-edits")
                print("TestPrice",i)
                print("Test Failed since attempted input out of bounds")
            
            elif i > 10000:
                self.type("#price", float(i))
                self.click("#submit-edits")
                print("TestPrice",i)
                print("Test Failed since attempted input out of bounds")
            
        

    # def test_lastModifiedDateTest(self, *_):
    #     """
    #     R5-3, Tests that last_date_modified updated when operation
    #     is successful.
    #     Will be using output coverage for this. 
    #     """
    #     testUser = db.session.query(User) \
    #         .filter_by(email="artielomonaco@email.com").first()
    #     base_url = 'http://127.0.0.1:{}'.format(5000)
    #     self.open(base_url + "/profile/" + str(testUser.id))
    #     # SIGNING IN
    #     self.type("#email", "artielomonaco@email.com")
    #     self.type("#password", "ianDasouza1!")
    #     self.click('#login-button')
    #     self.open(base_url + "/profile/" + str(testUser.id))
    #     self.click("#") #BlackBox testcity


    # def test_followsAboveRequirements(self, *_):
    #     """
    #     R5-4, Tests that when updating an attribute, one has to make
    #     sure that it follows the same requirements as above.
    #     """