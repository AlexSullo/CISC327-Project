from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from qbnb import *
from qbnb.models import *
import random

greetings = [
    'Hey there',
    'Hi',
    'Welcome',
    'How are you'
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
        }
        pickedGreeting = random.choice(greetings)
        return render_template('profile.html',
                               userData=userData,
                               greeting=pickedGreeting)

@app.route("/update/<id>", methods=['POST'])
def update_profile(id):
    '''
    Allows user to update their profile
    '''
    pass


if __name__ == '__ main__':
    app.run()