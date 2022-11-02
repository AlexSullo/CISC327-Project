from qbnb import *
from qbnb.models import *
from qbnb_test import *
import random
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
    return testUser.id


# TESTS

'''
NOTE:
R2 tests do not actually log in the user, as we use
flask_login to log the user in. It does, however,
validate the email/password combination which is
when we run the flask_login login function in regular
QBNB.
'''


def r2_1_fail():
    '''
    Test that tests case R2_1 and intentionally fails.
    User should not be able to log in if email and password
    do not match.

    USES:

    '''
    user = db.session.query(User) \
        .filter_by(email="automatedtestuser@email.com").first()


def r2_1_pass():
    '''
    Test that tests case R2_1 and passes.
    User should be able to log in as email and password will
    match.

    USES:

    '''
    user = db.session.query(User) \
        .filter_by(email="automatedtestuser@email.com").first()


def r2_2_fail():
    '''
    Test that tests case R2_2 and intentionally fails.
    The function that validates the email/password combination
    should test the inputted values against the RegEx used for
    registration. In this case, it should not work. (User won't
    be able to sign in because password will be wrong.)

    USES:
    Input Partition + Shotgun Testing
    PARTITIONS:
            --- PASSWORD REGEX ---
    Correct Email & Correct Password - Invalid Regex 
            (capitalization will be incorrect)
    Correct Email & Incorrect Password - Invalid Regex 
            (password will be RNG'd)
    Correct Email & Incorrect Password - Valid Regex
            
            --- EMAIL REGEX ---
    Incorrect Email & Correct Password - Invalid Regex

    Incorrect Email & Incorrect Password - Invalid Regex
            (password passes RegEx)
    Incorrect Email & Incorrect Password - Valid Regex
            (password passes RegEx)
    '''
    choicesStr = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    choicesStr += '0123456789!#@-'
    invalRegExPass = 'testedpassword1!'  # No capitals
    valRegExPass = ' passWord1!2woohoo'  # Meets RegEx
    invalRegExEmail = "woohoo!!!@@@email.com"  # Not an email
    valRegExEmail = "thisisnotmyemail@email.com"  # Meets RegEx
    user = db.session.query(User) \
        .filter_by(email="automatedtestuser@email.com").first()
    passwordLen = random.randint(8, 16)
    rngPassword = ''  # The randomly-generated password
    for x in range(passwordLen):
        val = random.randint(1, len(choicesStr))
        key = choicesStr[val - 1]
        rngPassword += key

    print("Testing password Regex...")
    attempt = user.login("automatedtestuser@email.com", invalRegExPass)
    assert user.authenticated is False
    print("CORRECT EMAIL & CORRECT PASSWORD W/ INVALID REGEX:", attempt)
    attempt = user.login("automatedtestuser@email.com", rngPassword)
    assert user.authenticated is False
    print("CORRECT EMAIL & INCORRECT PASSWORD W/ INVALID REGEX:", attempt)
    attempt = user.login("automatedtestuser@email.com", valRegExPass)
    assert user.authenticated is False
    print("CORRECT EMAIL & INCORRECT PASSWORD W/ VALID REGEX:", attempt)
    
    print("\nTesting email Regex...")
    attempt = user.login(invalRegExEmail, "testedPassword1!")
    assert user.authenticated is False
    print("INCORRECT EMAIL & CORRECT PASSWORD W/ INVALID REGEX:", attempt)
    attempt = user.login(invalRegExEmail, valRegExPass)
    assert user.authenticated is False
    print("INCORRECT EMAIL & INCORRECT PASSWORD W/ INVALID REGEX:", attempt)
    attempt = user.login(valRegExEmail, valRegExPass)
    assert user.authenticated is False
    print("INCORRECT EMAIL & INCORRECT PASSWORD W/ VALID REGEX:", attempt)
    r2_2_pass()


def r2_2_pass():
    '''
    Test that tests case R2_2 and passes.
    The function that validates the email/password combination
    should test the inputted values against the RegEx used for
    registration. (User will be able to sign in.)
    
    USES:
    Input Partition + Shotgun Testing (cont. from R2_2_fail())
    Correct Password - Valid Regex
    '''
    user = db.session.query(User) \
        .filter_by(email="automatedtestuser@email.com").first()
    attempt = user.login("automatedtestuser@email.com", "testedPassword1!")
    print("-- CORRECT PASSWORD & VALID REGEX --", attempt)
    assert user.username == 'automateduser'
    assert user.authenticated is True
    print("\nR2_2 Tests complete.")

# TEARDOWN


def delete_test_user():
    '''
    Deletes the test user from the database
    '''
    user = db.session.query(User) \
        .filter_by(email="automatedtestuser@email.com").first()
    db.session.delete(user)
    db.session.commit()


'''
SERVER FUNCTIONS
'''


def shutdown():
    '''
    Shuts down the server
    '''
    db.session.close()


'''
ACTUAL TESTING
'''


createNewUser()
r2_2_fail()
delete_test_user()
shutdown()
