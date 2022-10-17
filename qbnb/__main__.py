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
    email = "sebsemail@email.com"
    password = "password"
    attemptedUser = db.session.query(User).filter(User.email == email).first()
    print("attempted user:")
    print(attemptedUser.email)
    print(attemptedUser.password)
    print("---")
    print(email)
    print(password)
    attempt = attemptedUser.login(email, password)
    print(attempt)
    return render_template("register.html",
                           login=True)


if __name__ == '__ main__':
    app.run()
