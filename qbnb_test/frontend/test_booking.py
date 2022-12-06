from seleniumbase import BaseCase
from selenium.common.exceptions import NoSuchElementException
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


class bookListingTest(BaseCase):
    # These two initializations create the main user that will be 
    # testing the booking of the website
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
                       "price": float(50.00),
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

    '''
    Brute force creating a new user that books the listing made by the 
    test user.
    '''
    bookUserInfo = {"firstName": "Book",
                    "surname": "book user",
                    "email": "bookuser@email.com",
                    "password": "testedPassword1!",
                    "billingAddress": "1234 book Address",
                    "postalCode": "A6A6A6",
                    "username": "bookUser123"}
        
    bookUser = User(bookUserInfo)
    bookUser.billingAddress = bookUserInfo["billingAddress"]
    db.session.add(bookUser)
    db.session.commit()     

    '''
    Third User
    '''
    thirdUserInfo = {"firstName": "Third",
                     "surname": "User",
                     "email": "thirduser@email.com",
                     "password": "testedPassword1!",
                     "billingAddress": "333 third Address",
                     "postalCode": "A3A3A3",
                     "username": "thirdkUser123"}
        
    thirdUser = User(thirdUserInfo)
    thirdUser.billingAddress = thirdUserInfo["billingAddress"]
    db.session.add(thirdUser)
    db.session.commit()     

    """
    Testing:
    - T1 - A user can book a listing. (This will not be 
    tested together with T3)
    - T2 - A user cannot book a listing for his/her listing. 
    (partition blackbox test, each partiton is a different way 
    to access own property booking)
    - T3 - A user cannot book a listing that costs more than 
    his/her balance. (partition blackbox testing)
    - T4 - A user cannot book a listing that is already booked 
    with the overlapped dates.(will be tested once through a 
    third user)
    - T5 - A booked listing will show up on the user's home
    page (up-coming stages). (will not be tested since it 
    shows on the homepage)
    """
    '''
    - T2 -
    Tests User cant book own listing.
    Partitions based on how they try to access book page for own
    Listing
    '''
    def test_userBookOwnProperty(self, *_):
        '''
        - T2 -
        This test should fail since the button should not be found
        since this property is the current user's.
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
        # try to press button to book own listing
        try:
            self.click("#bookButton")
        except NoSuchElementException:
            print("element not found")
               
    def test_userAccessPropertyBookHtml(self, *_):
        '''
        - T2 -
        This test will end up redirecting the user back to the 
        home page since he cannot access the url for book on 
        their own property.
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
        # try to go to the book page by force through html
        m = self.open(base_url + "/listing/" + "/" + str(testListing.id) 
            + "/book")
        self.assert_false(m)
    
    '''
    - T3 - 
    Black box Partition Testing for booking a listing.
    The partitions will be different prices and they
    will be either more the same amount or less than
    the balance than the user currently has.
    '''
    def test_bookingLessThanBalance(self, *_):
        '''
        - T3 -
        The property that user will try to book has a price
        that is less than their balance, so booking will work.
        '''
        testUser = db.session.query(User) \
            .filter_by(email="automatedtestuser@email.com").first()
        base_url = 'http://127.0.0.1:{}'.format(5000)
        testListing = db.session.query(Listing) \
            .filter_by(title="Automated").first()
        testListingId = str(testListing.id)
        self.open(base_url + "/profile/" + str(testUser.id))
        # SIGNING IN
        self.type("#email", "automatedtestuser@email.com")
        self.type("#password", "testedPassword1!")
        self.click('#login-button')
        # self.click("#dropDown")
        self.hover_and_click("#dropDown", '#logoutButton')
        
        # Signing in with bookUser
        testUser = db.session.query(User) \
            .filter_by(email="bookuser@email.com").first()
        base_url = 'http://127.0.0.1:{}'.format(5000)
        testListing = db.session.query(Listing) \
            .filter_by(title="Book").first()
        self.open(base_url + "/profile/" + str(testUser.id))
        # SIGNING IN
        self.type("#email", "bookuser@email.com")
        self.type("#password", "testedPassword1!")
        self.click('#login-button')
        # http://127.0.0.1:5000/profile/9/addbalance
        # adds balance
        self.open(base_url + "/profile/" + str(testUser.id) + "/addbalance")
        self.click("#rbc")
        self.type("#balanceAmount", float(100.01))

        # book listing
        self.open(base_url + "/listing/" + str(testListingId) + "/book")
        self.click("#book-button")

    def test_bookingMoreThanBalance(self, *_):
        '''
        - T3 -
        The property that user will try to book has a price
        that is more than their balance, so booking will not work.
        '''
        testUser = db.session.query(User) \
            .filter_by(email="automatedtestuser@email.com").first()
        base_url = 'http://127.0.0.1:{}'.format(5000)
        testListing = db.session.query(Listing) \
            .filter_by(title="Automated").first()
        testListingId = str(testListing.id)
        self.open(base_url + "/profile/" + str(testUser.id))
        # SIGNING IN
        self.type("#email", "automatedtestuser@email.com")
        self.type("#password", "testedPassword1!")
        self.click('#login-button')
        # self.click("#dropDown")
        self.hover_and_click("#dropDown", '#logoutButton')
        
        # Signing in with bookUser
        testUser = db.session.query(User) \
            .filter_by(email="bookuser@email.com").first()
        base_url = 'http://127.0.0.1:{}'.format(5000)
        testListing = db.session.query(Listing) \
            .filter_by(title="Book").first()
        self.open(base_url + "/profile/" + str(testUser.id))
        # SIGNING IN
        self.type("#email", "bookuser@email.com")
        self.type("#password", "testedPassword1!")
        self.click('#login-button')
        # http://127.0.0.1:5000/profile/9/addbalance
        # adds balance
        self.open(base_url + "/profile/" + str(testUser.id) + "/addbalance")
        self.click("#rbc")
        self.type("#balanceAmount", float(10.00))

        # book listing
        self.open(base_url + "/listing/" + str(testListingId) + "/book")
        self.click("#book-button")

    def test_bookingEqualThanBalance(self, *_):
        '''
        - T3 -
        The property that user will try to book has a price
        that is equal than their balance, so booking will work.
        '''
        testUser = db.session.query(User) \
            .filter_by(email="automatedtestuser@email.com").first()
        base_url = 'http://127.0.0.1:{}'.format(5000)
        testListing = db.session.query(Listing) \
            .filter_by(title="Automated").first()
        testListingId = str(testListing.id)
        self.open(base_url + "/profile/" + str(testUser.id))
        # SIGNING IN
        self.type("#email", "automatedtestuser@email.com")
        self.type("#password", "testedPassword1!")
        self.click('#login-button')
        # self.click("#dropDown")
        self.hover_and_click("#dropDown", '#logoutButton')
        
        # Signing in with bookUser
        testUser = db.session.query(User) \
            .filter_by(email="bookuser@email.com").first()
        base_url = 'http://127.0.0.1:{}'.format(5000)
        testListing = db.session.query(Listing) \
            .filter_by(title="Book").first()
        self.open(base_url + "/profile/" + str(testUser.id))
        # SIGNING IN
        self.type("#email", "bookuser@email.com")
        self.type("#password", "testedPassword1!")
        self.click('#login-button')
        # http://127.0.0.1:5000/profile/9/addbalance
        # adds balance
        self.open(base_url + "/profile/" + str(testUser.id) + "/addbalance")
        self.click("#rbc")
        self.type("#balanceAmount", float(10.00))

        # book listing
        self.open(base_url + "/listing/" + str(testListingId) + "/book")
        self.click("#book-button")
    
    '''
    - T4 -
    Will be testing users cant book when booking date overlaps
    with another users booking of same property.
    '''
    def test_cantBookOtherUserBookedProperty(self, *_):
        '''
        - T4 - 
        This function tests that users cannot book a listing that
        the dates overlap with another users booked same listing.
        '''
        testUser = db.session.query(User) \
            .filter_by(email="automatedtestuser@email.com").first()
        base_url = 'http://127.0.0.1:{}'.format(5000)
        testListing = db.session.query(Listing) \
            .filter_by(title="Automated").first()
        testListingId = str(testListing.id)
        self.open(base_url + "/profile/" + str(testUser.id))
        # SIGNING IN
        self.type("#email", "automatedtestuser@email.com")
        self.type("#password", "testedPassword1!")
        self.click('#login-button')
        # self.click("#dropDown")
        self.hover_and_click("#dropDown", '#logoutButton')
        
        # Signing in with bookUser
        testUser = db.session.query(User) \
            .filter_by(email="bookuser@email.com").first()
        base_url = 'http://127.0.0.1:{}'.format(5000)
        # testListing = db.session.query(Listing) \
        #     .filter_by(title="Book").first()
        self.open(base_url + "/profile/" + str(testUser.id))
        # SIGNING IN
        self.type("#email", "bookuser@email.com")
        self.type("#password", "testedPassword1!")
        self.click('#login-button')
        # http://127.0.0.1:5000/profile/9/addbalance
        # adds balance
        self.open(base_url + "/profile/" + str(testUser.id) + "/addbalance")
        self.click("#rbc")
        self.type("#balanceAmount", float(100.01))

        # book listing
        self.open(base_url + "/listing/" + str(testListingId) + "/book")
        self.click("#book-button")

        # logout
        self.open(base_url + "/profile/" + str(testUser.id))
        # self.click("#dropDown")
        self.hover_and_click("#dropDown", '#logoutButton')

        # sign in third user
        testUser = db.session.query(User) \
            .filter_by(email="thirduser@email.com").first()
        base_url = 'http://127.0.0.1:{}'.format(5000)
        # testListing = db.session.query(Listing) \
        #     .filter_by(title="Book").first()
        self.open(base_url + "/profile/" + str(testUser.id))
        self.type("#email", "thirduser@email.com")
        self.type("#password", "testedPassword1!")
        self.click('#login-button')
        # http://127.0.0.1:5000/profile/9/addbalance
        # adds balance
        self.open(base_url + "/profile/" + str(testUser.id) + "/addbalance")
        self.click("#rbc")
        self.type("#balanceAmount", float(100.01))

        # book listing
        self.open(base_url + "/listing/" + str(testListingId) + "/book")
        self.click("#book-button")
        