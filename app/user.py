import sys
from random import randint
from app import db

class User(db.Document):
    phoneNumber= db.StringField("User Phone Number")#hash(number)
    rndSeed = db.IntField()#random seed to gnerate passowrds
    oneTimeKey = db.IntField()#negative if not active

    
    @staticmethod
    def newUser(number):
        pass

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
def getCode():
    return randint(10000,999999)

def getRandomSeed():
    return randint(-system.maxint - 1, sys.maxint)
