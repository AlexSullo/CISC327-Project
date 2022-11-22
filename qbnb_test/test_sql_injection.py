from qbnb.models import *


def test_sql_injection():
    with open('qbnb_test/sql-injection-payload-list.txt', 'r') as file:
        for payload in file:
            print("Payload:", payload)
            # SQL INJECTION TESTING: REGISTER (registration in models.py)
            # try to register with payload as the username
            userData = {
                "username": payload,
                "email": "randomemail@email.com",
                "password": "testedPassword1!"
            }
            try:
                User.registration(userData)
            except Exception as error:
                print("Exception error for username payload:", str(error))
            # try to register with payload as the email
            userData = {
                "username": "testuser",
                "email": payload,
                "password": "testedPassword1!"
            }
            try:
                User.registration(userData)
            except Exception as error:
                print("Exception error for email payload:", str(error))
            # try to register with payload as the password
            userData = {
                "username": "testuser",
                "email": "randomemail@email.com",
                "password": payload
            }
            try:
                User.registration(userData)
            except Exception as error:
                print("Exception error for password payload:", str(error))
            # SQL INJECTION TESTING: LISTING
            listingData = {"title": payload,
                           "description": "This is a test but \
                           should be longer than the title",
                           "price": "200"}
            try:
                Listing.__init__(listingData).checkListing()
            except Exception as error:
                print("Exception error for title payload:", str(error))
            listingData = {"title": "this place",
                           "description": payload,
                           "price": "200"
                          }
            try:
                Listing.__init__(listingData).checkListing()
            except Exception as error:
                print("Exception error for description payload:", str(error))
            listingData = {"title": "this place",
                           "description": "This is a test but \
                           should be longer than the title",
                           "price": payload
                          }
            try:
                Listing.__init__(listingData).checkListing()
            except Exception as error:
                print("Exception error for description payload:", str(error))