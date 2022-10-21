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
    return render_template('homepage.html')


@app.route("/listing/<id>")
def listing(id):
    '''
    Loads the page of a listing based on its ID
    '''

    return render_template('listing.html')


@app.route('/profile/<int:id>', methods=['GET', 'POST'])
def profile(id):
    '''
    Allows user to view/update their profile
    '''
    if request.method == 'GET':
        user = db.session.query(User).get(id)
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
        }
        pickedGreeting = random.choice(greetings)
        return render_template('profile.html',
                               userData=userData,
                               greeting=pickedGreeting,
                               id=id)


@app.route("/update/<id>", methods=['GET', 'POST'])
def update_profile(id):
    '''
    Allows user to update their profile
    '''
    user = db.session.query(User).get(id)
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
        }
        return render_template('updateInfo.html',
                               userData=userData)
    else:
        try:
            if request.form['username'] != "":
                user.username = request.form['username']

            if request.form['email'] != "":
                user.email = request.form['email']

            if request.form['billingAddress'] != "":
                user.billingAddress = request.form['billingAddress']

            if request.form['postalCode'] != "":
                user.postalCode = request.form['postalCode'].upper()

            db.session.commit()
        except AttributeError:
            db.session.rollback()
            raise
    return redirect("/profile/" + str(id))


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
        print(register_user)
        if register_user == True:
            return render_template('profile.html')
        else:
            print("you stupid")
            render_template('register.html', message='You failed you dumb bitch!')
    return render_template('register.html', message='Final return')

    """
        email = request.form.get("email")
        attemptedUser = db.session.query(User).filter(email == email).first()
        attemptedUser.password = request.form['password']
        attempt = attemptedUser.registration(request.form['username'], request.form['password'], email)
        if attempt:
            newUser = User(username=request.form['username'],
                 email=request.form['email'],
                 firstName=request.form['firstName'],
                 password=request.form['password'],
                 surname=request.form['surname'],
                 billingAddress=request.form['billingAddress'],
                 postalCode=request.form['postalCode']
                  )
            db.session.add(newUser)
            db.session.commit()
            return redirect("/")
        print(attempt)
        """


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

   
