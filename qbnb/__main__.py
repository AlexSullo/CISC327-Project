import base64
from sqlite3 import IntegrityError
from flask import Flask, redirect, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import *
from qbnb import *
from curses.ascii import isalnum
from qbnb.models import *
import random

greetings = [
    'Hey there',
    'Hi',
    'Welcome',
    'Greetings'
]

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@app.route("/")
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
        listingData = {
            "owner": userInfo[0],
            "title": request.form["title"],
            "description": request.form["description"],
            "price": request.form["price"],
            "address": request.form["address"],
            "propertyType1": request.form["propertyType1"],
            "propertyType2": request.form["propertyType2"],
            "propertyType3": request.form["propertyType3"],
            "propertyType4": request.form["propertyType4"],
            "dateAvailable": request.form["dateAvailable"],
            "imgData": data,
            "imgRenderedData": render_file
        }
        newListing = Listing(listingData)  # Creates the new listing
        if newListing.checkListing():  # If valid redirects to new listing page
            # Renders listing template and passes through values
            return render_template('listing.html',
                                   owner=newListing.owner,
                                   title=newListing.title,
                                   description=newListing.description,
                                   price=newListing.price,
                                   address=newListing.address,
                                   pt1=newListing.propertyType1,
                                   pt2=newListing.propertyType2,
                                   pt3=newListing.propertyType3,
                                   pt4=newListing.propertyType4,
                                   date=newListing.dateAvailable,
                                   lmd=newListing.lastModifiedDate,
                                   file_render=newListing.imgRenderedData,
                                   booked=newListing.booked,
                                   rating=newListing.rating,
                                   reviews=newListing.reviews)
            # return redirect("/listing/" + newListing.__repr__())
        else:
            print("ERROR - LISTING NOT CREATED (see __main__.py create())")
            

@app.route("/listing/<id>", methods=['GET', 'POST'])
def listing(id):
    '''
    Loads the page of a listing based on its ID
    '''

    userInfo = get_info()  # Check if user is signed in
    return render_template('listing.html',
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
            "propertyReviews": ['Hello'],  # CHANGE
            "userReviews": user.userReview,
            "balance": user.balance
        }  # Get user information from DB
        print(userData)
        userInfo = get_info()  # Check if user is signed in
        return render_template('profile.html',
                               userData=userData,
                               greeting=pickedGreeting,
                               userInformation=userInfo[0],
                               user=userInfo[1],
                               idPass=idPass)


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
            "propertyReviews": user.propertyReview,
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
        print(attempt)
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


if __name__ == '__ main__':
    app.run()

   
