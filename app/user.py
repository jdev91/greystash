import sys
from random import randint
from app import db

class User(db.Document):
    uID = db.StringField("Secret phrase")#hash(User secret phrase)
    rndSeed = db.StringField("Seed number")#random seed to gnerate passowrds
    ursSeeds = db.DictField(db.StringField(),"URL salts")#table mapping URL to current salt

    
    def updateSalt(current):
        if current ==sys.maxint:
            return -sys.maxint
        return current + 1
    def getRandomInt():
        return randint(-(sys.maxint),sys.maxint)
    #monditory methods
    def is_authenticated(self):
        return True
    def is_active(self):
        return True
    def is_anonymous(self):
        return False
    def get_id(self):
        try:
            return unicode(sefl.id)
        except NameError:
            return str(self.id)
    def __repr__(self):
        return '<User %r seed %r>' % (self.uID,self.rndSeed)
