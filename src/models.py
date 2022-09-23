from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# setting up SQLAlchemy and data models so we can map data models into database tables
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, 
        primary_key=True
        )
    username = db.Column(db.String(80), 
        unique=True, 
        nullable=False
        )
    email = db.Column(db.String(120), 
        unique=True, 
        nullable=False
        )
    password = db.Column(db.String(120), 
        unique=True, 
        nullable=False
        )
    rating = db.Column(db.String(120), 
        unique=True, 
        nullable=False
        )
    propertyReview = db.Column(db.String(120), 
        unique=True, 
        nullable=False
        )
    userReview = db.Column(db.String(120), 
        unique=True, 
        nullable=False
        )


    def __repr__(self):
        return '<User %r>' % self.username


class Transaction(db.Model):
    """
    Holds all relevant information regarding a transaction in which a
    user books a listing. Holds the date, payee of the transaction,
    recipient of the transaction, and price of the transaction.
    """
    id = db.Column(db.Integer, 
        primary_key=True
        )
    DateOfTransaction = db.Column(db.DateTime,
        unique=False,
        nullable=False
        )
    payee = db.Column(User.id, 
        unique=False, 
        nullable = False
        )
    recipient = db.Column(User.id, 
        unique=False,
        nullable=False
        )
    transactionPrice = db.Column(db.Float, 
        unique=False,
        nullable=False
        )


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
        unique=True
        )
    booked = db.Column(db.Boolean,  # Determines if listing has been booked
        unique=False,
        nullable=False
        )
    address = db.Column(db.String(120),  # Address of the listing
        unique=True,
        nullable=False
        )
    owner = db.Column(User.id,  # Registered user who listed the property
        unique=False,
        nullable=False
        )
    propertyType = db.Column(db.String(80),  # The type of property
        unique=False,
        nullable=False
        )
    rating = db.Column(db.Float,  # The rating from 0.0 - 5.0
        unique=False,
        nullable=True
        )
    reviews = db.Column(db.String(120),  # The reviews of the listing
        unique=False,
        nullable=True
        )
    dateAvailable = db.Column(db.DateTime,  # Range when the property is available
        unique=False,
        nullable=False
        )
    costPerNight = db.Column(db.Float,  # The cost of the property per night
        unique=False,
        nullable=False
        )
    description = db.Column(db.String(360),  # The description area of the listing
        unique=False,
        nullable=True
        )
    coverImage = db.Column(db.String(120),  # The url for the image of the listing
        unique=False,
        nullable=False
        )

    
    def __repr__(self):
        """Returns the id of the listing.
        """
        return '<Listing %r>' % self.id