from sqlite3 import IntegrityError
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
            "surname": user.surname,
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


@app.route("/register", methods=['GET','POST'])
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
        register_user = User.registration(userData)
        if register_user == True:
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
