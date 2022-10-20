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
]

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@app.route("/", methods=['GET', 'POST'])
def home():
    '''
    Renders the homepage for QBNB
    '''
    userInfo = get_info()
    return render_template("homepage.html",
                           userInformation=userInfo[0],
                           user=userInfo[1])


@app.route("/logout")
def logout():
    '''
    Temporary function that will auto-log out the user by navigating to the
    URL.
    '''
    logout_user()
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
        }
        userInfo = get_info()
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
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        attemptedUser = db.session.query(User).filter(email == email).first()
        attempt = attemptedUser.login(email, password)
        if attempt:
            login_user(attemptedUser)        
            return redirect("/")
        else:
            userInfo = get_info()
            return render_template("register.html",
                                   login=True,
                                   message=attempt)
    else:
        return render_template("register.html",
                               login=True)


@login_manager.user_loader
def load_user(id):
    return db.session.query(User).get(id)


def get_info():
    '''
    A function that returns the current user's information if they are signed
    in
    '''
    user = db.session.query(User).get(current_user.get_id())
    if user is None:
        return [None, False]
    else:
        return [user, True]


if __name__ == '__ main__':
    app.run()
    
    