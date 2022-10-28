from curses.ascii import isalnum
import datetime
from flask import Flask, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from qbnb import app
import re


'''
setting up SQLAlchemy and data models so we can map data models into database
tables
'''

db = SQLAlchemy(app)


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True,
                   unique=True)

    username = db.Column(db.String(80),
                         unique=True,
                         nullable=False)

    email = db.Column(db.String(120),
                      unique=True,
                      nullable=False)

    password = db.Column(db.String(120),
                         unique=False,
                         nullable=False)

    rating = db.Column(db.String(120),
                       unique=False,
                       nullable=False)

    propertyReview = db.Column(db.String(120),
                               unique=False,
                               nullable=True)

    userReview = db.Column(db.String(120),
                           unique=False,
                           nullable=True)

    balance = db.Column(db.Float,
                        nullable=False)

    billingAddress = db.Column(db.String(120),
                               unique=False,
                               nullable=False)

    postalCode = db.Column(db.String(6),
                           unique=False,
                           nullable=False)
    
    firstName = db.Column(db.String(15),
                          unique=False,
                          nullable=False)

    surname = db.Column(db.String(20),
                        unique=False,
                        nullable=False)

    authenticated = db.Column(db.Boolean,
                              default=False)
        
    def registration(self, userData):
        reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*[@$!%*#?&])\
        [A-Za-z\d@$!#%*?&]{6,20}$"
        pat = re.compile(reg)
        mat = re.search(pat, userData['password'])
        if userData['username'] == "":
            print("Username can not be empty.")
            return False
        if userData['password'] == "":
            print("Password can not be empty.")
            return False

        passwordRules = [lambda s: any(
            x.isupper() for x in s), lambda s: any(
                x.islower() for x in s), lambda s: any(
                x.isdigit() for x in s),
            lambda s: len(s) >= 7]
        if not all(rule(userData['password']) for rule in passwordRules):
            print(userData['password'])
            return "Error, password does not meet required complexity"

        if len(userData['username']) < 2 or len(userData['username']) > 20:
            print("Username must be between 2 and 20 characters long")
            return False

        i = 0
        for c in userData['username']:
            if (i == 0 or i == len(userData['username']) - 1): 
                if (not c.isalnum()):  # If its not alphanumeric
                    print("Username: 'contains spaces on \
                    the ends or non-alphanumeric'")
                    return False
            elif (c == " "):  # Or if its a space within the title
                pass
            elif (not c.isalnum()):  # Or if its not alphanumeric
                print("'non-alphanumeric'")
                return False
            i += 1
        user = User(userData)
        user.billingAddress = userData['billingAddress']
        db.session.add(user)
        db.session.commit()
        return True

    def login(self, entered_email, entered_password):
        """
        Login function for the website. First checks if password/email
        are empty, meet, and that they meet email conventions and
        password complexoty before checking database. Checks database
        if email is in it, then checks if password meets the correct
        one in database.
        """
        # checks if email/password empty
        if not entered_email or not entered_password:
            return "Error, Email/password should not be empty"
        # checks if email meets addr-spec defined
        # in RFC 5322 convention using regex
        userAttempt = db.session.query(User).filter_by(email=entered_email)
        userAttempt = userAttempt.first()
        if entered_password != userAttempt.password:
            return 'Password is incorrect.'
        userAttempt = db.session.query(User).filter_by(email=entered_email)
        userAttempt = userAttempt.first()
        if entered_password != userAttempt.password:
            return 'Password is incorrect.'
        r = r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'
        regex = re.compile(r)
        if not re.fullmatch(regex, entered_email):
            return "Error, email does not follow RFC 5322 convention"
        # checks if password meets complexity standard using rules list
        passwordRules = [lambda s: any(
            x.isupper() for x in s), lambda s: any(
                x.islower() for x in s), lambda s: any(
                x.isdigit() for x in s),
            lambda s: len(s) >= 7]
        if not all(rule(entered_password) for rule in passwordRules):
            return "Error, password does not meet required complexity"
        # checks database if email in it
        SignInAttempt = db.session.query(User).filter(
            User.email == entered_email).first()
        if SignInAttempt:
            # once user email checked, checks if entered password
            # equals the password in database
            if SignInAttempt.password == entered_password:
                User.authenticated = True
                return "Login, Successful."
            else:
                return "Error, incorrect email and/or password, try again."
        else:
            return "Error, incorrect email and/or password, try again."

    def __repr__(self):
        return '<User %r>' % self.username

    def __init__(self, userInfo):
        self.firstName = userInfo['firstName']
        self.email = userInfo['email']
        self.password = userInfo['password']
        self.billingAddress = userInfo['billingAddress']
        self.postalCode = userInfo['postalCode']
        self.rating = '5.0'
        self.balance = 100.0
        self.propertyReview = ''
        self.userReview = '0'
        self.billingAddress = ''
        self.surname = userInfo['surname']
        self.username = userInfo['username']

    def save_updated_info(self, updatedInfo):
        '''
        Check if the user has updated any of the relevant fields, and if they
        have, update their information.
        '''
        if updatedInfo.username:
            self.username = updatedInfo.username

        if updatedInfo.email:
            self.email = updatedInfo.email

        if updatedInfo.billingAddress:
            self.billingAddress = updatedInfo.billingAddress

        if updatedInfo.postalCode:
            self.postalCode = updatedInfo.postalCode

        return '<User %r Updated.>' % self.id


class Transaction(db.Model):
    """
    Holds all relevant information regarding a transaction in which a
    user books a listing. Holds the date, payee of the transaction,
    recipient of the transaction, and price of the transaction.
    """
    __tablename__ = 'transactions'
    id = db.Column(db.Integer,  # Unique value to identify user
                   primary_key=True,
                   unique=True
                   )

    DateOfTransaction = db.Column(db.DateTime,  # Day/Time of trans.
                                  unique=False,
                                  nullable=False
                                  )

    payee = db.Column(db.String(20),  # Person who paid for the transaction
                      unique=False,
                      nullable=False)

    recipient = db.Column(db.String(20),  # Person who received transaction
                          unique=False,
                          nullable=False)

    transactionPrice = db.Column(db.Float,  # Price of the transaction
                                 unique=False,
                                 nullable=False
                                 )

    def __repr__(self):
        return '<Transaction %r>' % self.id


class Listing(db.Model):
    """A listing represents a property listed by a registered user who
    is designated as the owner of the listing. A listing is bookable
    by a registered user who is not the owner. A listing holds the
    address of the property, the registered user who listed the
    property (owner), the type of property, ratings and reviews of the
    property, the date it was listed, the cost per night, as well as
    pictures and a description.
    """

    __tablename__ = 'listings'
    id = db.Column(db.Integer,  # Unique number identifies the listing
                   primary_key=True,
                   unique=True,
                   nullable=False)

    title = db.Column(db.String(40),  # The title of the listing
                      nullable=False)

    description = db.Column(db.String(2000),  # The description area of listing
                            unique=False,
                            nullable=True)

    price = db.Column(db.Float,  # The cost of the property per night
                      unique=False,
                      nullable=False)

    lastModifiedDate = db.Column(db.String(60),  # The date changes were made
                                 unique=False,
                                 nullable=False)

    ownerId = db.Column(db.Integer,  # Unique number identifies the owner
                        primary_key=True,
                        unique=True)

    booked = db.Column(db.Boolean,  # Determines if listing has been booked
                       unique=False,
                       nullable=False)

    address = db.Column(db.String(120),  # Address of the listing
                        nullable=False)

    owner = db.Column(db.String(20),  # Registered user who listed the property
                      unique=False,
                      nullable=False)

    propertyType1 = db.Column(db.String(30),  # The type of building
                              unique=False,
                              nullable=False)

    propertyType2 = db.Column(db.String(30),  # Private/shared room/place
                              unique=False,
                              nullable=False)

    propertyType3 = db.Column(db.Integer,  # Number of bedrooms
                              unique=False,
                              nullable=False)

    propertyType4 = db.Column(db.Integer,  # Number of bathrooms
                              unique=False,
                              nullable=False)

    rating = db.Column(db.Float,  # The rating from 0.0 - 5.0
                       unique=False,
                       nullable=True)

    reviews = db.Column(db.String(120),  # The reviews of the listing
                        unique=False,
                        nullable=True)

    dateAvailable = db.Column(db.String(60),  # When the property is avail.
                              unique=False,
                              nullable=False)

    imgData = db.Column(db.LargeBinary,  # Actual data, needed for Download
                        nullable=False)

    imgRenderedData = db.Column(db.Text,  # Data to render the pic in browser
                                nullable=False)
    
    location = db.Column(db.String(32),  # Location (Area, province)
                         nullable=False)

    def __init__(self, listingData):
        if listingData['location'] != "":
            listingLoc = listingData['location']
        else:
            listingLoc = "Ontario, CAN"
        self.id = hash(listingData['title'])
        self.title = listingData['title']
        self.description = listingData['description']
        self.price = float(listingData['price'])
        self.lastModifiedDate = datetime.datetime.now()
        self.ownerId = hash(listingData['owner'])
        self.booked = False
        self.address = listingData['address']
        self.owner = str(listingData['owner'])
        self.propertyType1 = str(listingData['propertyType1'])
        self.propertyType2 = str(listingData['propertyType2'])
        self.propertyType3 = listingData['propertyType3']
        self.propertyType4 = listingData['propertyType4']
        self.rating = '5.0'
        self.reviews = ''
        self.location = listingLoc
        self.dateAvailable = str(listingData['dateAvailable'])
        self.imgData = listingData['imgData']
        self.imgRenderedData = listingData['imgRenderedData']

    def checkListing(self):
        """This function checks if the title, description, price, and
        last modified date are all up to the standards set by the
        customer. It returns False if one attribute breaks the rules
        and returns True if the listing is created and successfully
        passes all tests.
        """
        # CHECK TITLE
        i = 0
        titleLen = len(self.title)
        if (titleLen > 80):  # If the title exceeds 80 characters
            print("Listing Error: Title Error: '" + str(titleLen - 80) +
                  " characters above the limit of 80'")
            return False
        for c in self.title:
            if (i == 0 or i == titleLen - 1):  # First or last character
                if (not c.isalnum()):  # If its not alphanumeric
                    print("Listing Error: Title Error: 'contains spaces on " +
                          "the ends or non-alphanumeric'")
                    return False
            elif (c == " "):  # Or if its a space within the title
                pass
            elif (not c.isalnum()):  # Or if its not alphanumeric
                print("Listing Error: Title Error: 'non-alphanumeric'")
                return False
            i += 1
        # CHECK DESCRIPTION
        descLen = len(self.description)
        if (descLen <= titleLen):  # Description is not longer than the title
            print("Listing Error: Description Error: 'description must be " +
                  "longer than title'")
            return False
        if (descLen < 20 or descLen > 2000):  # Chars not within its boundaries
            print("Listing Error: Description Error: 'description must be " +
                  "between 20 and 2000 characters'")
            return False
        # CHECK PRICE
        if (self.price < 10 or self.price > 10000):  # Price outside of range
            print("Listing Error: Price Error: 'price must be between 10 " +
                  "and 10000 dollars per night'")
            return False
        # CHECK LAST MODIFIED DATE
        self.lastModifiedDate = datetime.datetime.now()  # Set to current day
        smallestDate = datetime.datetime(2021, 1, 2)  # yyyy/mm/dd format
        largestDate = datetime.datetime(2025, 1, 2)
        if (self.lastModifiedDate < smallestDate or
                self.lastModifiedDate > largestDate):
            print("Listing Error: Last Modified Date Error: 'date must be " +
                  "within 4 years from 2021-01-02'")
            return False
        return True

    def updateListing(self, t, d, p):
        """This function receives the updated values of the listing
        which includes the title, description, and price. It first
        checks the updated values by calling checkListing. If that
        returns false, the listing cannot be updated at this time
        and the function terminates.
        """
        # A new temp listing is created that contains updated values
        temp = Listing(title=t, description=d, price=p)
        # Checks if the listing with the updated values is valid
        flag = temp.checkListing()
        print("newList valid:", flag)
        if (not flag):
            return False
        # UPDATE TITLE
        if (t != self.title):
            self.title = t
            print("Title updated!")
        # UPDATE DESCRIPTION
        if (d != self.description):
            self.description = d
            print("Description updated!")
        # UPDATE PRICE
        if (p > self.price):
            self.price = p
            print("Price increased!")
        else:
            print("Listing Error: Price Error: 'updated price must be " +
                  "greater than original'")
            return False
        # UPDATE LAST MODIFIED DATE
        self.lastModifiedDate = datetime.datetime.now()
        return True

    def __repr__(self):
        """
        Returns the path name of the listing.
        """
        return str(self.title) + str(self.id)


class BankTransfer(db.Model):
    """
    Holds all of the data relevant to a transfer of funds to a user's account
    from their bank account.
    """
    __tablename__ = 'banktransfer'
    id = db.Column(db.Integer,
                   primary_key=True,
                   unique=True)

    dateOfTransaction = db.Column(db.DateTime,
                                  unique=False,
                                  nullable=False)

    bank = db.Column(db.String(6),
                     nullable=False)

    TransferUser = db.Column(db.String(20),
                             unique=False,
                             nullable=False)

    transactionAmount = db.Column(db.Float,
                                  unique=False,
                                  nullable=False)