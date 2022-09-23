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
    id = db.Column(db.Integer,  # Unique value to identify user
        primary_key=True,
        unique=True
        )
    DateOfTransaction = db.Column(db.DateTime,  # Day/Time of trans.
        unique=False,
        nullable=False
        )
    payee = db.Column(User.id,  # Person who paid for the transaction
        unique=False, 
        nullable = False
        )
    recipient = db.Column(User.id,  # Person who received transaction
        unique=False,
        nullable=False
        )
    transactionPrice = db.Column(db.Float,  # Price of the transaction
        unique=False,
        nullable=False
        )


    def __repr__(self):

        """
        Test function to return id of instance and object type
        """
        return '<Transaction %r>' % self.id


class BankTransfer(db.Model):
    """
    - Holds all of the data relevant to a transfer of funds to a user's account from their bank account.
    """
    id = db.Column(db.Integer, 
        primary_key=True,
        unique=True
        )
    dateOfTransaction = db.Column(db.DateTime,
        unique=False,
        nullable=False
        )
    bank = db.Column(db.String(6),
        nullable=False
        )
    TransferUser = db.Column(User.id, 
        unique=False, 
        nullable = False
        )
    transactionAmount = db.Column(db.Float, 
        unique=False
        nullable = False)

