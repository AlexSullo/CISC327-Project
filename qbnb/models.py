from curses.ascii import isalnum
import datetime
from enum import unique
from flask import Flask, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager
from qbnb import app
from flask_migrate import Migrate
from sqlalchemy.dialects.mysql import LONGBLOB, LONGTEXT
from email_validator import validate_email, EmailNotValidError
import re


'''
setting up SQLAlchemy and data models so we can map data models into database
tables
'''

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True,
                   unique=True)

    username = db.Column(db.String(80),  # Display name of user
                         unique=True,
                         nullable=False)

    email = db.Column(db.String(120),  # Email of user
                      unique=True,
                      nullable=False)

    password = db.Column(db.String(120),  # Password of user
                         unique=False,
                         nullable=False)

    rating = db.Column(db.String(120),  # Rating of User
                       unique=False,
                       nullable=False)

    writtenReviews = db.Column(db.Text,
                               unique=False,
                               nullable=True)

    reviewsAbout = db.Column(db.Text,
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

    bookedListings = db.Column(db.Text,  # List of booked listings
                               default="",
                               nullable=False)

    def registration(self, userData):
        reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*[@$!%*#?&])\
        [A-Za-z/d@$!#%*?&]{6,20}$"
        pat = re.compile(reg)
        mat = re.search(pat, userData['password'])
        if userData['email'] == "":
            return [False, "Email can not be empty."]
        else:
            email = db.session.query(User).filter_by(email=userData['email'])
            if email.first() is not None:
                return [False, "Email already in use."]
        if userData['username'] == "":
            return [False, "Username can not be empty."]
        if userData['password'] == "":
            return [False, "Password can not be empty."]

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
        is_new_account = True
        try:
            validation = validate_email(userData['email'],
                                        check_deliverability=is_new_account)
            email = validation.email
            user = User(userData)
            user.billingAddress = userData['billingAddress']
            user.bookedListings = ''
            db.session.add(user)
            db.session.commit()
            return True
        except EmailNotValidError as e:
            print(str(e))
            return False
    
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
            pass
            # return "Error, password does not meet required complexity"
        # checks database if email in it
        SignInAttempt = db.session.query(User).filter(
            User.email == entered_email).first()
        if SignInAttempt:
            # once user email checked, checks if entered password
            # equals the password in database
            if SignInAttempt.password == entered_password:
                User.authenticated = True
                return 'Login, Successful.'
            else:
                return "Incorrect email and/or password, try again."
        else:
            return "Incorrect email and/or password, try again."

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
        self.writtenReviews = ''
        self.reviewsAbout = ''
        self.billingAddress = ''
        self.surname = userInfo['surname']
        self.username = userInfo['username']
        self.bookedListings = ''

    def save_updated_info(self, updatedInfo):
        '''
        Check if the user has updated any of the relevant fields, and if they
        have, update their information.
        '''
        if updatedInfo.username:
            if 2 < len(updatedInfo.username) < 20:
                self.username = updatedInfo.username
            
        if updatedInfo.email:
            r = r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\
                .[A-Z|a-z]{2,})+'
            regex = re.compile(r)
            if not re.fullmatch(regex, updatedInfo.email):
                pass
            else:
                if len(db.session.query(User)
                   .filter_by(email=updatedInfo.email)).first() is None:
                    self.email = updatedInfo.email

        if updatedInfo.billingAddress:
            self.billingAddress = updatedInfo.billingAddress

        if updatedInfo.postalCode:
            r = r'^([A-Za-z]\d[A-Za-z][-]?\d[A-Za-z]\d)'
            regex = re.compile(r)
            if not re.fullmatch(regex, updatedInfo.postalCode):
                pass
            else:
                self.postalCode = updatedInfo.postalCode

        return '<User %r Updated.>' % self.id

    def getReviews(self):
        '''
        Returns all reviews written by and about a user
        '''
        writtenCheck = self.writtenReviews.split(",")
        aboutCheck = self.reviewsAbout.split(",")
        writtenCheck.reverse()
        aboutCheck.reverse()
        if len(writtenCheck) != 0 and writtenCheck[0] != "":
            written = []
            for x in writtenCheck:
                rev = db.session.query(Review).get(x) 
                written.append(rev)
        else:
            written = None
        if len(aboutCheck) != 0 and aboutCheck[0] != "":
            about = []
            for y in aboutCheck:
                rev = db.session.query(Review).get(y)
                about.append(rev)
        else:
            about = None
        return [written, about]


class Transaction(db.Model):
    """
    Holds all relevant information regarding a transaction in which a
    user books a listing. Holds the date, payee of the transaction,
    recipient of the transaction, and price of the transaction.
    """
    __tablename__ = 'transactions'
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True,
                   unique=True)

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

    def __init__(self, transactionInfo):
        '''
        Creates a Transaction object
        '''
        try:
            self.DateOfTransaction = datetime.datetime.now()
            self.payee = transactionInfo['payee']
            self.recipient = transactionInfo['recipient']
            self.transactionPrice = float(transactionInfo['amount'])
        except ValueError:
            return False

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
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True,
                   unique=True)

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
                        primary_key=False,
                        unique=False)

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

    reviews = db.Column(db.Text,  # The reviews of the listing
                        unique=False,
                        nullable=True)

    dateAvailable = db.Column(db.String(60),  # When the property is avail.
                              unique=False,
                              nullable=False)
    # Actual data, needed for download
    imgData = db.Column(db.LargeBinary,
                        nullable=False)
    # Data to render the pic in browser
    imgRenderedData = db.Column(db.Text,
                                nullable=False)
    
    location = db.Column(db.String(32),  # Location (Area, province)
                         nullable=False)

    tenants = db.Column(db.Text,
                        nullable=False)

    def __init__(self, listingData):
        if listingData['location'] != "":
            listingLoc = listingData['location']
        else:
            listingLoc = "Ontario, CAN"
        self.title = listingData['title']
        self.description = listingData['description']
        self.price = float(listingData['price'])
        self.lastModifiedDate = datetime.datetime.now()
        self.ownerId = listingData['owner']
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
        self.tenants = ''
    
    def createListing(self, listingData):
        '''
        Creating a create list functionl that allows the listingData
        parameter to be able to accept the payload input from
        the SQL injection. This is the case since the create
        listing function in controllers does not have any
        parameters that the injection can insert unless we
        run the website. Like the registration function in models
        doing the same thing to manually input the listingData
        '''
        # Checking that attributes meet requirements for test
        if listingData['owner'] == "":
            print("Property must have owner")
        if listingData['title'] == "" or re.match(
            '^[a-zA-Z0-9_]+$', listingData['email']) or len(
                listingData['title']) > 20:
            print("Title must be alphanumeric and can't be empty.")
            print("Or title must not be longer than 80char")
            return False
        if listingData['description'] == "" or len(
                listingData['description']) > 2000 or len(
                listingData['description'] < 20) or len(
                listingData['description']) < len(
                listingData['title']):
            print("Must be more than 20 characters")
            print("or must be less than 2000")
            return False
        if listingData['price'] < 10 or listingData[
           'price'] > 10000:
            print("Price must be more than 10")
            return False
        if listingData['address'] == "":
            print("address must not be empty")
            return False
        if listingData['propertyType1'] == "":
            print("Must not be empty")
            return False
        if listingData['propertyType2'] == "":
            print("Must not be empty")
            return False
        if listingData['propertyType3'] == "":
            print("Must not be empty")
            return False
        if listingData['propertyType4'] == "":
            print("Must not be empty")
            return False
        if listingData['location'] == "":
            print("Must not be empty")
            return False
        if listingData[
           'dateAvailable'] == datetime.time(0, 0):
            print("Date available must not be empty")
            return False
        d1 = datetime.datetime(2021, 1, 2, 0, 0, 0)
        d2 = datetime.datetime(2025, 1, 2, 0, 0, 0)
        if listingData['lastModifiedDate'] < d1 or listingData[
           'lastModifiedDate'] > d2:
            print("must be between 2021-01-02 and 2025-01-02")
            return False
        # requirements checked
        # listing created
        listing = Listing(listingData)
        db.session.add(listing)
        db.session.commit()
        return True        

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

    def getListing(self):
        '''
        Returns relevant modifiable data in a dictionary.
        '''
        self.check()  # Check if listing needs to be unbooked
        listingData = {
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "booked": self.booked,
            "address": self.address,
            "owner": self.owner,
            "dateAvailable": self.dateAvailable,
            "imgRenderedData": self.imgRenderedData
        }
        return listingData

    def __repr__(self):
        """
        Returns the id of the listing.
        """
        return '<Listing %r>' % self.id

    def getReviews(self):
        '''
        Returns all reviews about a listing
        '''
        reviews = []
        reviewCheck = self.reviews.split(",")
        if len(reviewCheck) != 0 and reviewCheck[0] != "":
            for review in reviewCheck:
                rev = db.session.query(Review).get(review)
                reviews.append(rev)
        reviews.reverse()
        return reviews
    
    def getReviewAuthors(self):
        '''
        Returns the ID of everyone who has written a review
        '''
        authors = []
        reviewCheck = self.reviews.split(",")
        print(reviewCheck)
        if len(reviewCheck) != 0 and reviewCheck[0] != "":
            for review in reviewCheck:
                print(review, "review")
                rev = db.session.query(Review).get(review)
                authors.append(rev.author)
        return authors

    def getPreviousTenants(self):
        '''
        Returns the ID of everyone who has stayed at the property
        '''
        tenants = []
        tenantCheck = self.tenants.split(",")
        if len(tenantCheck) != 0 and tenantCheck[0] != "":
            for tenant in tenantCheck:
                ten = db.session.query(User).get(tenant)
                tenants.append(ten.id)
        return tenants

    def updateRating(self):
        '''
        Updates the rating of a property
        '''
        try:
            allReviews = self.reviews.split(",")
            print(allReviews)
            numOfReviews = len(allReviews)
            overallRating = 0
            for review in allReviews:
                review = db.session.query(Review).get(int(review))
                overallRating += review.rating
            overallRating /= numOfReviews  # Det. average rating
            self.rating = overallRating            
            db.session.commit()  # Save updated Review in DB
        except AttributeError:
            # No Reviews
            self.rating = 5.0
            return 'No Reviews'

        except ValueError:
            # Also no reviews
            self.rating = 5.0

    def detNights(self):
        '''
        Determines the number of nights a stay will be.
        '''
        dates = self.dateAvailable.split(" to ")
        d1 = dates[0].split("-")
        d2 = dates[1].split("-")
        try:
            d1 = datetime.date(int(d1[0]), int(d1[1]), int(d1[2]))
            d2 = datetime.date(int(d2[0]), int(d2[1]), int(d2[2]))
            date = d2 - d1
            return str(date)[:-14]
        except ValueError:  # day is out of range for month
            date = 'NaT'
            return date
            
    def bookListing(self, bookingInfo):
        '''
        Books the listing
        '''
        if self.booked is False:
            tenant = bookingInfo['tenant']
            if tenant.balance - bookingInfo['total'] < 0:
                return 'Error'
            else:
                if len(self.tenants) == 0:
                    self.tenants += str(tenant.id)
                else:
                    self.tenants += "," + str(tenant.id)
                if len(tenant.bookedListings) == 0:
                    tenant.bookedListings += str(self.id)
                else:
                    tenant.bookedListings += "," + str(self.id)
                self.booked = True
                tenant.balance -= bookingInfo['total']
                ownerUser = db.session.query(User).get(self.ownerId)
                ownerUser.balance += bookingInfo['total']
            db.session.commit()
            return 'Success'
        
        else:
            return 'Error'

    def check(self):
        '''
        Automatically unbooks a listing if it is past the date of 
        availability and it was booked.
        '''
        dates = self.dateAvailable.split(" to ")
        d2 = dates[1].split("-")
        d2 = datetime.datetime(int(d2[0]), int(d2[1]), int(d2[2]))
        print(d2, "date4")
        present = datetime.datetime.now()
        print(present, "present")
        print(present < d2)
        print(d2 < present)
        if d2 < present:
            self.booked = False  # Unbook listing
            try:
                newestTenant = self.tenants.split(",")[-1]
                tenant = db.session.query(User).get(newestTenant)
                tenantListings = tenant.bookedListings
                splitTenant = tenantListings.split(",")
                if len(splitTenant) == 1:
                    tenant.bookedListings = ''
                else:
                    del (splitTenant[-1])
                    newBookedListings = ''
                    for x in splitTenant:  # Update user's booked listings
                        if len(newBookedListings) == 0:
                            newBookedListings += str(x)
                        else:
                            newBookedListings += "," + str(x)
                    tenant.bookedListings = newBookedListings
            except AttributeError:  # Empty tenants list
                pass
        db.session.commit()
        

class BankTransfer(db.Model):
    """
    Holds all of the data relevant to a transfer of funds to a user's account
    from their bank account.
    """
    __tablename__ = 'banktransfer'
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True,
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

    def __init__(self, data):
        '''
        Creates a BankTransfer object
        '''
        try:
            self.dateOfTransaction = datetime.datetime.now()
            self.bank = data['bank']
            self.TransferUser = data['user']
            self.transactionAmount = float(data['amount'])
        except ValueError:
            return None


class Review(db.Model):
    '''
    An object that contains a review, either about a property, or a user.

    author: Author of the review (User id)
    authorName: Name of Author (str)
    reviewType: What the review is about (Host/Tenant/Property) (str)
    recipient: Who the review is about (User id or Listing id)
    content: Content of the review (str)
    rating: Number rating of the recipient (float)
    '''
    __tablename__ = 'reviews'
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True,
                   unique=True)

    author = db.Column(db.String(32),  # Author of review
                       nullable=False)

    authorName = db.Column(db.String(64),
                           nullable=False)

    reviewType = db.Column(db.String(32),  # Type of review
                           nullable=False)

    recipient = db.Column(db.String(32),  # Who/What
                          nullable=False)

    content = db.Column(db.Text,  # Content of the review
                        nullable=False)

    rating = db.Column(db.Float,  # Rating of the Review
                       nullable=False)

    date = db.Column(db.String(32),  # Date of Writing
                     nullable=False)

    def __init__(self, reviewData):
        '''
        Construct the Review Object

        reviewData: Dictionary object containing all information
                    required to construct the review. (Dict)
        '''
        if reviewData['author'] != "" and reviewData['author'] != "" \
            and reviewData['recipient'] != "" \
                and reviewData['rating'] != "":
            # If no fields are empty
            auth = db.session.query(User).get(reviewData['author'])
            authorName = auth.firstName + " " + auth.surname
            # Creates a string that has the name of the author
            
            self.authorName = authorName
            self.author = reviewData['author']
            self.reviewType = reviewData['type']
            self.recipient = reviewData['recipient']
            self.rating = reviewData['rating']
            self.content = reviewData['content']
            self.date = datetime.date.today()
    
    def updateTables(self):
        '''
        Updates the database
        '''
        auth = db.session.query(User).get(self.author)
        if self.reviewType == "Property":
            # If the review is on a property
            listing = db.session.query(Listing) \
                .filter_by(id=self.recipient).first()
            if len(listing.reviews) == 0:
                listing.reviews += str(self.id)  # Append review
            else:
                listing.reviews += "," + str(self.id)  # Append review

            if len(auth.writtenReviews) == 0:
                auth.writtenReviews += str(self.id)  # Append rev.
            else:
                auth.writtenReviews += "," + str(self.id)  # Append rev.
            listing.updateRating()
            db.session.commit()

        elif (
            self.reviewType == 'Host' or
            self.reviewType == 'Tenant'
        ):
            # Review is on a user
            user = db.session.query(User).get(self.recipient)
            if len(user.reviewsAbout) == 0:
                user.reviewsAbout += str(self.id)  # Append review
            else:
                user.reviewsAbout += "," + str(self.id)  # Append review

            if len(auth.writtenReviews) == 0:
                auth.writtenReviews += str(self.id)  # Append rev.
            else:
                auth.writtenReviews += "," + str(self.id)  # Append rev.

            db.session.commit()
        else:
            return 'Missing Information.'

    def deleteReview(self, requester):
        '''
        Deletes the review object if the requestor is the creator

        requestor: ID of the user requesting deletion. (int)
        '''
        if str(requester) == str(self.author):
            # Requester of deletion is author of review
            if self.reviewType == "Property":
                recipient = db.session.query(Listing) \
                    .filter_by(id=int(self.recipient)).first()

                # Remove Review from Property's Reviews
                reviews = recipient.reviews.split(",")
                loc = reviews.index(str(self.id))
                del (reviews[loc])
                if len(reviews) == 1:
                    recipient.reviews = reviews[0]
                else:
                    revString = ''
                    for x in reviews:
                        revString += x + ","
                    recipient.reviews = revString[:-1]
            else:
                recipient = db.session.query(User) \
                    .filter_by(id=int(self.recipient)).first()

                # Remove Review from Recipient's Reviews
                reviews = recipient.reviewsAbout.split(",")
                loc = reviews.index(str(self.id))
                del (reviews[loc])
                if len(reviews) == 1:
                    recipient.reviews = reviews[0]
                else:
                    revString = ''
                    for x in reviews:
                        revString += x + ","
                    recipient.reviews = revString[:-1]
            
            # Remove review from Author's Reviews
            author = db.session.query(User).get(int(self.author))
            reviews = author.writtenReviews.split(",")
            loc = reviews.index(str(self.id))
            del (reviews[loc])
            if len(reviews) == 1:
                author.writtenReviews = reviews[0]
            else:
                revString = ''
                for x in reviews:
                    revString += x + ","
                author.writtenReviews = revString[:-1]
                
            db.session.delete(self)
            db.session.commit()  # Update DB
            return 'Review Deleted'
        else:  # Requester is not author of Review
            return 'Denied.'


db.create_all()