'''
Required for the folder to be considered a module
'''
from flask import Flask
from flask_login import LoginManager


def create_app():
    '''
    Starts up the app
    '''
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'aaalsatechnologieszz11223344alsatechnologies'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../db.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    return app


app = create_app()


def __init__(self, listingData):
    if listingData['location'] != "":
        listingLoc = listingData['location']
    else:
        listingLoc = "Ontario, CAN"
    self.id = hash(listingData['title'])
    self.title = listingData['title']
    self.description = listingData['description']
    self.price = float(listingData['price'])
    self.lastModifiedDate = datetime.datetime.now()
    self.ownerId = hash(listingData['owner'])
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
