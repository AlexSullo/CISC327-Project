from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# setting up SQLAlchemy and data models so we can map data models into database tables
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

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