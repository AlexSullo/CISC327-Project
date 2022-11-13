import base64
from flask import Flask, redirect, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import *
from curses.ascii import isalnum
from werkzeug.exceptions import BadRequestKeyError
import random
from qbnb import app
from qbnb.models import *
import collections

greetings = [
    'Hey there',
    'Hi',
    'Welcome',
    'Greetings'
]

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


def load_listings():
    '''
    Loads listings to show in homepage
    '''
    return db.session.query(Listing).all()


@app.route("/", methods=["GET","POST"])
def home():
    '''
    Renders the homepage for QBNB
    '''
    try:
        if request.method == "POST":
            search()
        else:
            listings = load_listings()
            userInfo = get_info()  # Check if user is signed in
            return render_template("homepage.html",
                                listings=listings,
                                userInformation=userInfo[0],
                                user=userInfo[1])
    except BadRequestKeyError:
        listings = load_listings()
        userInfo = get_info()  # Check if user is signed in
        return render_template("homepage.html",
                            listings=listings,
                            userInformation=userInfo[0],
                            user=userInfo[1])


@app.route("/profile/<id>/addbalance", methods=["GET", "POST"])
@login_required
def addbalance(id):
    '''
    Allows the signed in user to add to their balance
    '''
    userInfo = get_info()
    if str(current_user.get_id()) == str(id):  # User is on their page
        if request.method == "GET":
            return render_template("modifybalance.html",
                                   userInformation=userInfo[0],
                                   user=userInfo[1])
        elif request.method == "POST":
            if request.form['amount'] != "":
                # User did not enter an amount
                amount = request.form['amount']
            else:
                amount = '0.00'

            try:
                transactionInfo = {"amount": amount,
                                   "bank": request.form['bank'],
                                   "user": userInfo[0].id}
            
            except BadRequestKeyError:
                # User did not pick a bank
                transactionInfo = {"amount": amount,
                                   "bank": 'Money Order',
                                   "user": userInfo[0].id}
            newTransfer = BankTransfer(transactionInfo)
            if newTransfer:
                userInfo[0].balance += float(amount)
                if newTransfer.transactionAmount != 0.00:
                    # Does not add transaction to database if there is
                    # no amount.
                    db.session.add(newTransfer)
                    db.session.commit()
                return redirect("/profile/" + str(id))
            else:
                return render_template("404.html",
                                       userInformation=userInfo[0],
                                       user=userInfo[1])
    else:
        return render_template("404.html",
                               userInformation=userInfo[0],
                               user=userInfo[1])


@app.route("/logout")
def logout():
    '''
    Logs out the user.
    '''
    logout_user()  # Logs out the user
    return redirect("/")


@app.route("/create", methods=['GET', 'POST'])
@login_required
def create():
    '''
    Loads the page to create listing
    '''
    userInfo = get_info()  # Checks if user is signed in
    if request.method == 'GET':
        return render_template('create.html',
                               userInformation=userInfo[0],
                               user=userInfo[1])
    elif request.method == 'POST':
        file = request.files['inputFile']
        data = file.read()
        render_file = render_picture(data)
        date = request.form["dateAvailableStart"] + " to " 
        date += request.form["dateAvailableEnd"]
        listingData = {
            "owner": userInfo[0].id,
            "title": request.form["title"],
            "description": request.form["description"],
            "price": float(request.form["price"]),
            "address": request.form["address"],
            "propertyType1": request.form["propertyType1"],
            "propertyType2": request.form["propertyType2"],
            "propertyType3": request.form["propertyType3"],
            "propertyType4": request.form["propertyType4"],
            "dateAvailable": date,
            "location": request.form["location"],
            "imgData": data,
            "imgRenderedData": render_file
        }
        newListing = Listing(listingData)  # Creates the new listing
        db.session.add(newListing)  # Adds listing to database
        db.session.commit()
        if newListing.checkListing():  # If valid redirects to new listing page
            # Renders listing template and passes through values
            return redirect("/listing/" + str(newListing.id))
            # return redirect("/listing/" + newListing.__repr__())
        else:
            print("ERROR - LISTING NOT CREATED (see __main__.py create())")
            return redirect("/create")
            

@app.route("/listing/<id>", methods=['GET', 'POST'])
def listing(id):
    '''
    Loads the page of a listing based on its ID
    '''
    newListing = db.session.query(Listing).filter_by(id=id).first()
    listingOwner = (db.session.query(User).get(newListing.owner))
    newListing.updateRating()
    reviews = newListing.getReviews()
    try:
        if int(current_user.get_id()) in newListing.getPreviousTenants():
            
            # Checks if user has stayed at the property
            print("User in tenants")
            if str(current_user.get_id()) not in newListing.getReviewAuthors():
                # Checks if user has already reviewed the property
                print("User not in reviewers") 
                reviewer = True  # user can review property
            else:
                reviewer = False  # User can't review property
        else:
            reviewer = False  # user can't review property
    except TypeError:
        # User not signed in
        reviewer = False
    print("Reviewer:" + str(reviewer))
    try:
        if str(current_user.get_id()) == str(listingOwner.id):
            # Checks if signed in user is owner of profile
            idPass = True
        else:
            idPass = False
    except TypeError:
        # User not signed in
        idPass = False
    ownerStr = listingOwner.firstName + " " + listingOwner.surname
    listingData = {"owner": ownerStr,
                   "id": newListing.id,
                   "title": newListing.title,
                   "description": newListing.description,
                   "price": newListing.price,
                   "address": newListing.address,
                   "pt1": newListing.propertyType1,
                   "pt2": newListing.propertyType2,
                   "pt3": newListing.propertyType3,
                   "pt4": newListing.propertyType4,
                   "date": newListing.dateAvailable,
                   "lmd": newListing.lastModifiedDate,
                   "file_render": newListing.imgRenderedData,
                   "booked": newListing.booked,
                   "rating": newListing.rating,
                   "reviews": newListing.reviews}
    userInfo = get_info()  # Check if user is signed in
    return render_template('listing.html',
                           listingData=listingData,
                           userInformation=userInfo[0],
                           user=userInfo[1],
                           idPass=idPass,
                           reviewer=reviewer,
                           propertyReviews=reviews)


@app.route("/listing/<id>/book", methods=['GET', 'POST'])
@login_required
def book_listing(id):
    '''
    Allows the user to book a listing.
    '''
    newListing = db.session.query(Listing).filter_by(id=id).first()
    listingOwner = (db.session.query(User).get(newListing.owner)) 
    userInfo = get_info()
    listingOwner = listingOwner.firstName + " " + listingOwner.surname
    return render_template("bookListing.html",
                           listing=newListing,
                           owner=listingOwner,
                           userInformation=userInfo[0],
                           user=userInfo[1],
                           nights=1)


@app.route("/deletereview/<id>")
@login_required
def delete_review(id):
    review = db.session.query(Review).get(id)
    revType = review.reviewType
    revRec = review.recipient
    review.deleteReview(str(current_user.get_id()))
    if revType == "Property":
        return redirect("/listing/" + str(revRec))
    else:
        return redirect("/profile/" + str(revRec))


@app.route("/postreview/<id>/<revType>", methods=["GET", "POST"])
@login_required
def post_review(id, revType):
    if revType == '1':
        # Property Review
        userInfo = get_info()  # Get signed in user info
        newListing = db.session.query(Listing).filter_by(id=id).first()
        listingOwner = (db.session.query(User).get(newListing.owner)) 
        if request.method == "GET":
            
            listingOwner = listingOwner.firstName + " " + listingOwner.surname
            return render_template("createReview.html",
                                   revType=revType,
                                   listing=newListing,
                                   owner=listingOwner,
                                   userInformation=userInfo[0],
                                   user=userInfo[1])
        
        elif request.method == "POST":
            if request.form['rating'] == "":
                # User did not put a rating
                rating = "5.0"
            else:
                # User did put a rating
                rating = request.form['rating']
            reviewData = {"author": str(current_user.get_id()),
                          "recipient": str(newListing.id),
                          "rating": rating,
                          "type": 'Property',
                          "content": request.form['content']}

            newReview = Review(reviewData)
            db.session.add(newReview)
            db.session.commit()
            return redirect("/listing/" + str(newListing.id))

        else:
            return render_template("404.html",
                                   userInformation=userInfo[0],
                                   user=userInfo[1])
    
    if revType == '2' or revType == '3':
        # Property Review
        userInfo = get_info()  # Get signed in user info
        user = db.session.query(User).get(id)
        if request.method == "GET":
            
            return render_template("createReview.html",
                                   revType=revType,
                                   listing=user,
                                   owner=listingOwner,
                                   userInformation=userInfo[0],
                                   user=userInfo[1])
        
        elif request.method == "POST":
            if request.form['rating'] == "":
                # User did not put a rating
                rating = "5.0"
            else:
                # User did put a rating
                rating = request.form['rating']
            reviewData = {"author": str(current_user.get_id()),
                          "recipient": str(newListing.id),
                          "rating": rating,
                          "type": 'Property',
                          "content": request.form['content']}
            newReview = Review(reviewData)
            db.session.add(newReview)
            db.session.commit()
            return redirect("/listing/" + str(newListing.id))

        else:
            return render_template("404.html",
                                   userInformation=userInfo[0],
                                   user=userInfo[1])


@app.route('/profile/<int:id>', methods=['GET', 'POST'])
@login_required
def profile(id):
    '''
    Allows user to view a profile, and if it's their own, update it.
    '''
    if request.method == 'GET':
        user = db.session.query(User).get(id)
        userReviews = user.getReviews()
        if str(current_user.get_id()) == str(id):
            # Checks if signed in user is owner of profile
            idPass = True
            pickedGreeting = random.choice(greetings)
        else:
            idPass = False
            pickedGreeting = ""
        userData = {
            "username": user.username,
            "email": user.email,
            "billingAddress": user.billingAddress,
            "postalCode": user.postalCode,
            "firstName": user.firstName,
            "surname": user.surname,
            "rating": user.rating,
            "propertyReviews": user.writtenReviews,  # CHANGE
            "userReviews": user.reviewsAbout,
            "balance": user.balance
        }  # Get user information from DB
        userInfo = get_info()  # Check if user is signed in
        return render_template('profile.html',
                               userData=userData,
                               greeting=pickedGreeting,
                               userInformation=userInfo[0],
                               user=userInfo[1],
                               reviewsAbt=userReviews[1],
                               writtenRevs=userReviews[0],
                               idPass=idPass)


@app.route("/updatelisting/<id>", methods=['GET', 'POST'])
@login_required
def update_listing(id):
    '''
    Allows the user to update information about their listing, generally
    just the information that is changeable on websites like air bnb. Will be 
    able to change fields like price, description, but won't be able to 
    change fields like owner or listing id since the owner is you the user,
    and the listing id shouldn't be changed for any reason.
    '''
    listing = db.session.query(Listing).filter_by(id=id).first()
    if str(listing.ownerId) == str(current_user.get_id()):
        # idPass = True
        if request.method == 'GET':
            # Gets the listing ID
            # Dictionary of what should be changeable in a 
            # Listing from a user
            print(listing.propertyType1)
            listingInfo = {
                "title": listing.title,
                "description": listing.description,
                "price": listing.price,
                "booked": listing.booked,
                "address": listing.address,
                "dateAvailable": listing.dateAvailable,
                "imgData": listing.imgData,
                "coverImage": listing.imgRenderedData,
                "propertyType1": listing.propertyType1,
                "propertyType2": listing.propertyType2,
                "propertyType3": listing.propertyType3,
                "propertyType4": listing.propertyType4,
                "location": listing.location}
            userData = get_info()
            return render_template('updateListing.html',
                                   userInformation=userData[0],
                                   user=userData[1],
                                   listingInfo=listingInfo)
        elif request.method == "POST":
            # Listing info that can be changed by the owner
            print(request.form)
            if request.form['title'] != "":
                listing.title = request.form['title']

            if request.form['description'] != "":
                listing.description = request.form['description']

            if request.form['price'] != "":
                listing.price = request.form['price']
                
            if request.form['address'] != "":
                listing.address = request.form['address']
            try: 
                if request.form['booked'] != "":
                    listing.booked = request.form['booked']
            except BadRequestKeyError:
                pass
            
            try:
                if request.form['imgRenderedData']:
                    listing.imgRenderedData = request.form["imgRenderedData"]
            except BadRequestKeyError:
                pass
              
            if request.form['dateAvailable'] != "":
                listing.dateAvailable = request.form['dateAvailable']

            if request.form['propertyType1'] != "":
                listing.propertyType1 = request.form['propertyType1']

            if request.form['propertyType2'] != "":
                listing.propertyType2 = request.form['propertyType2']
            
            if request.form['propertyType3'] != "":
                listing.propertyType3 = request.form['propertyType3']
            
            if request.form['propertyType4'] != "":
                listing.propertyType4 = request.form['propertyType4']

            if request.form['location'] != "":
                listing.location = request.form['location']
                
            db.session.commit()
        return redirect("/updatelisting/" + str(id))
    else:
        # idPass = False
        return redirect("/listing/" + str(id))


@app.route("/update/<id>", methods=['GET', 'POST'])
@login_required
def update_profile(id):
    '''
    Allows user to update their profile
    '''
    user = db.session.query(User).get(id)  # Get profile id
    if request.method == 'GET':
        userData = {
            "username": user.username,
            "email": user.email,
            "billingAddress": user.billingAddress,
            "postalCode": user.postalCode,
            "firstName": user.firstName,
            "rating": user.rating,
            "balance": user.balance,
            "id": id
        }  # Get user data from database
        userInfo = get_info()  # Check if user is signed in
        return render_template('updateInfo.html',
                               userData=userData,
                               userInformation=userInfo[0],
                               user=userInfo[1])
    else:
        try:
            # Checks if the user entered new information or not
            if request.form['username'] != "":
                user.username = request.form['username']

            if request.form['email'] != "":
                user.email = request.form['email']

            if request.form['billingAddress'] != "":
                user.billingAddress = request.form['billingAddress']

            if request.form['postalCode'] != "":
                user.postalCode = request.form['postalCode'].upper()

            db.session.commit()  # Updates the database w/ new info
        except AttributeError:
            db.session.rollback()  # Undoes updating of DB
            raise
    return redirect("/profile/" + str(id))  # Reload profile


@app.route("/search", methods=["POST"])
def search():
    '''
    Potential function that will allow the user to search
    '''
    print("SEARCHIGN")
    if request.method == "POST":
        print("post")
        tag = request.form["search"]
        search = "%{}%".format(tag)
        listingsTitle = db.session.query(Listing).filter(Listing.title.like(search))
        listingsLoc = db.session.query(Listing).filter \
            (Listing.location.like(search))
        results = []
        for x in listingsTitle:
            results.append(x)
        for y in listingsLoc:
            results.append(x)
        results_clean = ([item for item, \
            count in collections.Counter(results).items() if count > 1])
        userInfo = get_info()
        return render_template("searchResults.html",
                            results=results_clean,
                            userInformation=userInfo[0],
                            user=userInfo[1])


@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        userData = {
            'username': request.form["username"],
            'password': request.form["password"],
            'firstName': request.form["firstName"],
            'surname': request.form["surname"],
            'email': request.form["email"],
            'billingAddress': request.form["billingAddress"],
            'postalCode': request.form["postalCode"]
        }
        register_user = User(userData).registration(userData)
        if register_user:
            login_user(db.session.query(User).filter_by(
                email=request.form["email"]).first())
            return redirect("/")
        else:
            render_template('register.html',
                            message='Your username or email is already' +
                                    'taken. Please try another one.')
    return render_template('register.html', message="Create your Account!")


@app.route("/login", methods=["GET", "POST"])
def login():
    '''
    Allows the user to login to their account
    '''
    if request.method == "POST":
        # Verify the information given by the user
        email = request.form.get("email")
        password = request.form.get("password")
        attemptedUser = db.session.query(User).filter_by(email=str(email))
        attemptedUser = attemptedUser.first()  # So that code matches PEP8
        attempt = attemptedUser.login(email, password)
        if attempt == 'Login, Successful.':
            # If email/password combo is correct
            login_user(attemptedUser)        
            return redirect("/")
        else:
            return render_template("register.html",
                                   login=True,
                                   message=attempt)
    else:
        return render_template("register.html",
                               login=True)


@login_manager.user_loader
def load_user(id):
    '''
    Function required for login manager
    '''
    return db.session.query(User).get(id)


def get_info():
    '''
    A function that returns the current user's information if they are signed
    in, and returns other information if they aren't. This function is for
    the navbar.
    '''
    user = db.session.query(User).get(current_user.get_id())
    if user is None:
        return [None, False]
    else:
        return [user, True]


def render_picture(data):
    '''
    A function that renders the given listing picture.
    '''
    render_pic = base64.b64encode(data).decode('ascii') 
    return render_pic