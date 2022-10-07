from flask import Flask, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
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
                   unique=True)

    DateOfTransaction = db.Column(db.DateTime,  # Day/Time of trans.
                                  unique=False,
                                  nullable=False)

    payee = db.Column(db.String(20),  # Person who paid for the transaction
                      unique=False, 
                      nullable=False)

    recipient = db.Column(db.String(20),  # Person who received transaction
                          unique=False,
                          nullable=False)

    transactionPrice = db.Column(db.Float,  # Price of the transaction
                                 unique=False,
                                 nullable=False)

    def __repr__(self):
        return '<Transaction %r>' % self.id


class Listing(db.Model):
    """
    A listing represents a property listed by a registered user who
    is designated as the owner of the listing. A listing is bookable
    by a registered user who is not the owner. A listing holds the 
    address of the property, the registered user who listed the 
    property (owner), the type of property, ratings and reviews of the
    property, the date it was listed, the cost per night, as well as
    pictures and a description.
    """
    __tablename__ = 'listings'
    id = db.Column(db.Integer,  # Unique number identifies the user
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

    costPerNight = db.Column(db.Float,  # The cost of the property per night
                             unique=False,
                             nullable=False)

    description = db.Column(db.String(360),  # The description area of listing
                            unique=False,
                            nullable=True)

    coverImage = db.Column(db.String(120),  # The url for the image of listing
                           unique=False,
                           nullable=False)

    def __repr__(self):
        """
        Returns the id of the listing.
        """
        return '<Listing %r>' % self.id


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

