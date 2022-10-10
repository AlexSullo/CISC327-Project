from qbnb import *
from qbnb.models import *
from qbnb_test import *
from qbnb_test.conftest import test_db
from flask import Flask, redirect, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy


'''
USER TESTS
'''

# SETUP


def createNewUser():
    '''
    Creates a new user to test the User functionalities in a test database.
    '''
    testUser = User('testuser', 'Sir Testsalot', 'testy@email.com', 'password')
    test_db.session.add(testUser)
    test_db.session.commit()
    return testUser.id

# TESTS


def updateInformation(id):
    '''
    Tests the ability to update a user's information as of Sprint 2
    '''
    user = test_db.session.query(User).get(id=id)
    oldUserData = {
        "username": user.username,
        "email": user.email,
        "billingAddress": user.billingAddress,
        "postalCode": user.postalCode
    }
    print("User\'s Current Information:")
    print(oldUserData)
    newusername = "Sir Nevertests"
    newemail = "neveremail@email.com"
    newAddress = "100 Address Street"
    newPostal = "K7L3N6"
    print("\nUpdating Info...")
    user.username = newusername
    user.email = newemail
    user.billingAddress = newAddress
    user.postalCode = newPostal
    test_db.commit()

# TEARDOWN


def delete_test_user(id):
    '''
    Deletes the test user from the database
    '''
    user = test_db.session.query(User).get(id=id)
    test_db.session.delete(user)
    test_db.session.commit()


'''
SERVER FUNCTIONS
'''


def shutdown():
    '''
    Shuts down the server
    '''
    test_db.session.close()


'''
ACTUAL TESTING
'''


userID = createNewUser()
updateInformation(userID)
delete_test_user(userID)
shutdown()
