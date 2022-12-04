from qbnb.models import *
from seleniumbase import BaseCase
from unittest.mock import patch
from qbnb.models import Listing, User, db
import datetime
from curses.ascii import isalnum
import base64
import os
import sys


def test_Booking():
    testUserInfoL = {"firstName": "Automated1",
                     "surname": "Testuser1",
                     "email": "automatedtestuser1@email.com",
                     "password": "testedPassword1!",
                     "billingAddress": "1212 Test Address",
                     "postalCode": "A1A1A1",
                     "username": "automateduser4"}       
    testUser1 = User(testUserInfoL)
    testUser1.billingAddress = testUserInfoL["billingAddress"]
    db.session.add(testUser1)
    testUser1 = db.session.query(User) \
        .filter_by(email="automatedtestuser1@email.com").first() 
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
    testUser = db.session.query(User) \
        .filter_by(email="automatedtestuser@email.com").first() 
    im = open(os.path.join(sys.path[0], "test.jpg"), "rb")
    data = im.read()
    render_pic = base64.b64encode(data).decode('ascii')
    date = str(datetime.datetime.now())[:10] + " to "
    date += "2022-02-12"
    testListingInfo = {"title": "Automated",
                       "owner": testUser1.id,
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
    test_Booking_Info ={"tenant": testUser1,
                        "total": 20.00}
    # testListing.imgRenderedData = testListing['imgRenderedData']
    db.session.add(testListing)
    testListing = db.session.query(Listing) \
        .filter_by(title="Automated").first() 
    testListing.bookListing(test_Booking_Info)
    db.session.commit()
    assert testUser.bookedListings.split(",")[0] != 0

def test_toExpensive():
    testUser = db.session.query(User) \
        .filter_by(email="automatedtestuser@email.com").first() 
    testUser1 = db.session.query(User) \
        .filter_by(email="automatedtestuser1@email.com").first() 
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
    test_Booking_Info = {"tenant": testUser1,
                        "total": 2.00}
    # testListing.imgRenderedData = testListing['imgRenderedData']
    db.session.add(testListing)
    testListing = db.session.query(Listing) \
        .filter_by(title="Automated").first() 
    testListing.bookListing(test_Booking_Info)
    db.session.commit()
    assert testListing.bookListing(test_Booking_Info) == "Error"

def test_Own_Listing():
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
    test_Booking_Info = {"tenant": testUser,
                        "total": 20.00}
    # testListing.imgRenderedData = testListing['imgRenderedData']
    db.session.add(testListing)
    testListing = db.session.query(Listing) \
        .filter_by(title="Automated").first() 
    testListing.bookListing(test_Booking_Info)
    db.session.commit()
    assert testListing.bookListing(test_Booking_Info) == "Error"

def test_already_booked():
    testUserInfoA = {"firstName": "Automated2",
                     "surname": "Testuser2",
                     "email": "automatedtestuser2@email.com",
                     "password": "testedPassword1!",
                     "billingAddress": "1212 Test Address",
                     "postalCode": "A1A1A1",
                     "username": "automateduser2"}       
    testUser2 = User(testUserInfoA)
    testUser2.billingAddress = testUserInfoA["billingAddress"]
    db.session.add(testUser2)
    testUser2 = db.session.query(User) \
        .filter_by(email="automatedtestuser1@email.com").first()
    testUser = db.session.query(User) \
        .filter_by(email="automatedtestuser@email.com").first() 
    testUser1 = db.session.query(User) \
        .filter_by(email="automatedtestuser1@email.com").first() 
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
    test_Booking_Info = {"tenant": testUser1,
                        "total": 100.00}
    test_Booking_Info2 = {"tenant": testUser2,
                         "total": 100.00}
    # testListing.imgRenderedData = testListing['imgRenderedData']
    db.session.add(testListing)
    testListing = db.session.query(Listing) \
        .filter_by(title="Automated").first() 
    testListing.bookListing(test_Booking_Info)
    testListing.bookListing(test_Booking_Info2)
    db.session.commit()
    assert testListing.bookListing(test_Booking_Info2) == "Error"




