from curses.ascii import isalnum
import datetime
from enum import unique
from flask import Flask, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user
from qbnb import app


'''
setting up SQLAlchemy and data models so we can map data models into database
tables
'''

db = SQLAlchemy(app)


class User(db.Model):
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

    def login(self, entered_email, entered_password):
        SignInAttempt = db.session.query(User).filter(
            User.email == entered_email).first()
        if SignInAttempt:
            if SignInAttempt.password == entered_password:
                User.authenticated = True
                return "Login, Successful."
            else:
                return "Error, incorrect email and/or password, try again."
        else:
            return "Error, incorrect email and/or password, try again."

    def __repr__(self):
        return '<User %r>' % self.username

    def __init__(self, username, firstName, email, password):
        self.firstName = firstName
        self.email = email
        self.password = password
        self.rating = '5.0'
        self.balance = 100.0
        self.propertyReview = ''
        self.userReview = ''
        self.billingAddress = ''
        self.postalCode = ''
        self.surname = ''
        self.username = username

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
    listingId = db.Column(db.Integer,  # Unique number identifies the listing
                          primary_key=True,
                          unique=True,
                          nullable=False)

    title = db.Column(db.String(40),  # The title of the listing
                      unique=True,
                      nullable=False)
    
    description = db.Column(db.String(2000),  # The description area of listing
                            unique=False,
                            nullable=True)

    price = db.Column(db.Float,  # The cost of the property per night
                      unique=False,
                      nullable=False)

    lastModifiedDate = db.Column(db.DateTime,  # The date changes were made
                                 unique=False,
                                 nullable=False)

    ownerId = db.Column(db.Integer,  # Unique number identifies the owner
                        primary_key=True,
                        unique=True)

    booked = db.Column(db.Boolean,  # Determines if listing has been booked
                       unique=False,
                       nullable=False)

    address = db.Column(db.String(120),  # Address of the listing
                        unique=True,
                        nullable=False)

    owner = db.Column(db.String(20),  # Registered user who listed the property
                      unique=False,
                      nullable=False)

    propertyType = db.Column(db.String(80),  # The type of property
                             unique=False,
                             nullable=False)

    rating = db.Column(db.Float,  # The rating from 0.0 - 5.0
                       unique=False,
                       nullable=True) 

    reviews = db.Column(db.String(120),  # The reviews of the listing
                        unique=False,
                        nullable=True)

    dateAvailable = db.Column(db.DateTime,  # Range when the property is avail.
                              unique=False,
                              nullable=False)

    coverImage = db.Column(db.String(120),  # The url for the listing image
                           unique=False,
                           nullable=False) 

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
        Returns the id of the listing.
        """
        return '<Listing %r>' % self.listingId


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
# Sprint 2: Listing Test Code
# oldT = "This is a sample title"
# oldD = "This is a sample description for testing purposes."
# oldP = 99.99
# oldList = Listing(title=oldT,description=oldD,price=oldP)
# print("oldList valid:", oldList.checkListing())
# newT = "This is the updated title"
# newD = "This is the updated description for testing purposes."
# newP = 100.99
# print("newList updated:", oldList.updateListing(newT, newD, newP))