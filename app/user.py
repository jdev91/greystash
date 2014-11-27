import sys
from random import randint
from app import db

INVALID_KEY = -1

class User(db.Document):
    phoneNumber= db.StringField("User Phone Number")#hash(number)
    rndSeed = db.IntField()#random seed to gnerate passowrds
    oneTimeKey = db.IntField()#negative if not active

    

    #monditory methods
    def is_authenticated(self):
        return True
    def is_active(self):
        return True
    def is_anonymous(self):
        return False
    def get_id(self):
        try:
            return unicode(self.id)
        except NameError:
            return str(self.id)
    def __repr__(self):
        return '<User %r seed %r>' % (self.phoneNumber,self.rndSeed)
def newUser(number):
    """
    Note:
        Number must be hashed already
    """
    if userExists(number):
        return None
    
    user =  User(phoneNumber=number,rndSeed=getRandomSeed(),oneTimeKey=INVALID_KEY)
    user.save()
    return user
def userExists(number):
   user = User.query.filter(User.phoneNumber == number).first()
   print("User:\n\t" + str(user))
   if user == None:
       return False
   return True
    
def getCode():
    return randint(10000,999999)

def getRandomSeed():
    return randint(-sys.maxint - 1, sys.maxint)
