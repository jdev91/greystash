import sys
from random import randint
from app import db

INVALID_KEY = -1

class User(db.Document):
    phoneNumber= db.StringField("User Phone Number")#hash(number)
    rndSeed = db.IntField()#random seed to gnerate passowrds
    oneTimeKey = db.IntField()#negative if not active
    
    def __repr__(self):
        return '<User %r seed %r>' % (self.phoneNumber,self.rndSeed)

def getUser(number):
    """ Find user in database

    Params:
        number: hashed phonenumber

    Returns:
        User object or None

    """
    return User.query.filter(User.phoneNumber == number).first()  

def newUser(number):
    """ Create new users if does not already exist

    Params:
        number: hashed phone number
    
    Returns:
        New user object or None if user already exists

    """
    if userExists(number):
        return None
    user =  User(phoneNumber=number,rndSeed=getRandomSeed(),oneTimeKey=INVALID_KEY)
    user.save()
    return user

def userExists(number):
    """ Checks for user in database
    
    Params:
        number: hashed phone number

    Returns:
        True if user exists false if not.

    """
    user = getUser(number)
    print("User:\n\t" + str(user))
    if user == None:
        return False
    return True
    
def getCode():
    """ Helper function to generate a random verification code """
    return randint(10000,999999)

def getRandomSeed():
    """ Generate a random integer for generating passwords uniquely for each user"""
    return randint(-sys.maxint - 1, sys.maxint)
