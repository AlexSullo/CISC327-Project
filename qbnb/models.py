from cgi import print_environ_usage
from enum import unique
from flask import Flask
from email_validator import validate_email, EmailNotValidError
# from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import false
import re


'''
setting up SQLAlchemy and data models so we can map data models into database
tables
    '''
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, 
                   primary_key=True,
                   unique=True)

    username = db.Column(db.String(80), 
                         unique=True, 
                         nullable=False)

    email = db.Column(db.String(120), 
                      unique=True, 
                      nullable=False)

    password = db.Column(db.String(120), 
                         unique=True, 
                         nullable=False)

    rating = db.Column(db.String(120), 
                       unique=True, 
                       nullable=False)

    propertyReview = db.Column(db.String(120), 
                               unique=True, 
                               nullable=False)
    
    shippingAddress = db.Column(db.String(120),
                                unique=False,
                                nullable=True)

    postalCode = db.Column(db.String(120),
                           unique=False,
                           nullable=True)

    balance = db.Column(db.Integer(),
                        unique=False,
                        nullable=False)

    userReview = db.Column(db.String(120), 
                           unique=True, 
                           nullable=False)
        
    def registration(self, username, password, email):
        reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*[@$!%*#?&])\
        [A-Za-z\d@$!#%*?&]{6,20}$"
        pat = re.compile(reg)
        mat = re.search(pat, password)
        if username == "":
            print("Username can not be empty.")
        if password == "":
            print("Password can not be empty.")
        if not mat:
            print("password is invalid, must contain one lower, \
            one upper, one special char and at least 6 characters long")
        if len(username) < 2 or len(username) > 20:
            print("Username must be between 2 and 20 characters long")
        i = 0
        for c in username:
            if (i == 0 or i == len(username) - 1): 
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
        self.balance = 100
        try:
            # Check that the email address is valid.
            validation = validate_email(email, check_deliverability=unique)  
            email = validation.email
        except EmailNotValidError as e:
            # Email is not valid.
            print(str(e))

        def __repr__(self):
            return '<User %r>' % self.username


class Transaction(db.Model):
    """
    Holds all relevant information regarding a transaction in which a
    user books a listing. Holds the date, payee of the transaction,
    recipient of the transaction, and price of the transaction.
    """
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


"""
* Sprint two: user registration
* Checks all cases to insure the account is made correctly
* Initializes balance to 100

pas = "alexSulloin"
ema = "alexsullo67@gmail.com"
use = "SuBooks"
user = User(username=use, password=pas, email=ema)
print(user.registration(use, pas, ema))
"""



