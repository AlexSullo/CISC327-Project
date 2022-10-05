from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from .models import User


app = Flask(__name__)


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


@app.route("/settings")
def settings():
    '''
    Opens the settings page
    '''

    return render_template('settings.html')

@app.route("/profile/<id>")
def view_profile(id):
    '''
    Allows user to view their profile
    '''
    print('Loading user')
    currentUser = User.query.get(1) # Change to id when testing done
    data = currentUser.send_user_info()
    print(data.username)
    return render_template('profile.html')

@app.route("/update/<id>", methods=['POST'])
def update_profile(id):
    '''
    Allows user to update their profile
    '''
    pass


if __name__ == '__ main__':
    app.run()