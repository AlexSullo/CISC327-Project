from flask import Flask, redirect, render_template, jsonify, request
from flask_login import *
from qbnb import *
from qbnb.models import *
from curses.ascii import isalnum
import random

greetings = [
    'Hey there',
    'Hi',
    'Welcome',
    'Greetings'
]  # Greetings for profile

# Set up Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@app.route("/", methods=['GET', 'POST'])
def home():
    '''
    Renders the homepage for QBNB
    '''
    userInfo = get_info()  # Check if user is signed in
    return render_template("homepage.html",
                           userInformation=userInfo[0],
                           user=userInfo[1])


@app.route("/logout")
def logout():
    '''
    Logs out the user.
    '''
    logout_user()  # Logs out the user
    return redirect("/")


@app.route("/listing/<id>")
def listing(id):
    '''
    Loads the page of a listing based on its ID
    '''

    return render_template('listing.html')


@app.route('/profile/<int:id>', methods=['GET', 'POST'])
@login_required
def profile(id):
    '''
    Allows user to view a profile, and if it's their own, update it.
    '''
    if request.method == 'GET':
        user = db.session.query(User).get(id)
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
            "rating": user.rating,
            "propertyReviews": ['Hello'],  # CHANGE
            "userReviews": user.userReview,
            "balance": user.balance
        }  # Get user information from DB
        userInfo = get_info()  # Check if user is signed in
        return render_template('profile.html',
                               userData=userData,
                               greeting=pickedGreeting,
                               userInformation=userInfo[0],
                               user=userInfo[1],
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
    listing = db.session.query(Listing).get(id)
    if str(listing.ownerId) == str(current_user.get_id()):
        if request.method == 'GET':
            # Gets the listing ID
            # Dictionary of what should be changeable in a 
            # Listing from a user
            listingInfo = {
                "title": listing.title,
                "description": listing.description,
                "price": listing.price,
                "booked": listing.booked,
                "address": listing.address,
                "owner": listing.owner,
                "dateAvailable": listing.dateAvailable,
                "coverImage": listing.coverImage}

            listingInfo = listing.getListing()
            userData = get_info()
            return render_template('updateListing.html',
                                   userInformation=userData[0],
                                   user=userData[1],
                                   listingInfo=listingInfo)
        elif request.method == "POST":
            # Listing info that can be changed by the owner
            if request.form['title'] != "":
                listing.title = request.form['title']

            if request.form['description'] != "":
                listing.description = request.form['description']

            if request.form['price'] != "":
                listing.price = request.form['price']
            
            if request.form['owner'] != "":
                listing.owner = request.form["owner"]
                
            if request.form['address'] != "":
                listing.address = request.form['address']
                
            if request.form['booked'] != "":
                listing.booked = request.form['booked']
            
            if request.form['imgData'] != "":
                listing.imgData = request.form["imgData"]

            if request.form['imgRenderedData'] != "":
                listing.imgRenderedData = request.form["imgRenderedData"]
            
            if request.form['dateAvailable'] != "":
                listing.dateAvailable = request.form['dateAvailable']

            if request.form['proprtyType1'] != "":
                listing.proprtyType1 = request.form['proprtyType1']

            if request.form['proprtyType2'] != "":
                listing.proprtyType2 = request.form['proprtyType2']
            
            if request.form['proprtyType3'] != "":
                listing.proprtyType3 = request.form['proprtyType3']
            
            if request.form['proprtyType4'] != "":
                listing.proprtyType4 = request.form['proprtyType4']

            if request.form['location'] != "":
                listing.location = request.form['location']
                
            db.session.commit()
        return redirect("/updatelisting/" + str(id))
    else:
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
            "propertyReviews": ['Hello'],  # CHANGE
            "userReviews": user.userReview,
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


@app.route("/register", methods=['GET', 'POST'])
def register():
    '''
    Allow a new user to register for an account
    '''
    return render_template("register.html",
                           login=False)


@app.route("/login", methods=["GET", "POST"])
def login():
    '''
    Allows the user to login to their account
    '''
    if request.method == "POST":
        # Verify the information given by the user
        email = request.form.get("email")
        password = request.form.get("password")
        attemptedUser = db.session.query(User).filter(email == email).first()
        attempt = attemptedUser.login(email, password)
        if attempt:
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


if __name__ == '__ main__':
    app.run()
    
    