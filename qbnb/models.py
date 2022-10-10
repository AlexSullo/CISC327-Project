from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user

'''
setting up SQLAlchemy and data models so we can map data models into database
tables
    '''
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, 
                   primary_key=True)

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

    userReview = db.Column(db.String(120), 
                           unique=True, 
                           nullable=False)
    
    authenticated = db.Column(db.Boolean, default=False)
    

    def login(self,entered_email,entered_password):
        SignInAttempt = db.session.query(User).get(entered_email)
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
