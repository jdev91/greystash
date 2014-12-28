import sys, re, copy
from random import randint
from app import db
from crypt import generatePassword

INVALID_KEY = -1
CURRENT = 0
NEXT = 1

class User(db.Document):
    phoneNumber= db.StringField("User Phone Number")#hash(number)
    rndSeed = db.IntField()#random seed to gnerate passowrds
    oneTimeKey = db.IntField()#negative if not active
    urlSalts = db.DictField(db.TupleField(db.IntField(), db.IntField()))#key url -> (currentSalt,NextSalt) 
    def __repr__(self):
        return '<User %r seed %r>' % (self.phoneNumber,self.rndSeed)

    def updateCode(self):
        code = getCode()
        self.oneTimeKey = code
        self.save()
        return code
    def checkCode(self,code):
        if code == self.oneTimeKey and code != INVALID_KEY:
            self.oneTimeKey = INVALID_KEY
            self.save()
            return True
        return False
    def getSalt(self, url, current = True):
        url = str(re.sub(r"[\.\$]","",url))
        #new URL or poorly formatted tuple
        if (not (url in self.urlSalts.keys())) or (len(self.urlSalts[url]) != 2):
            print("Have to make new salt: " + url)
            salt = getRandomSeed()
            nextSalt = getRandomSeed()
            self.urlSalts[url] = (salt, nextSalt)
            self.save()
        #figure out what salt we need
        print(str(self.urlSalts))
        index = NEXT
        if current:
            index = CURRENT
        return self.urlSalts[url][index]
    def updateSalt(self,url):
        url = re.sub(r"[\.\$]","",url)
        self.urlSalts[url] = (self.urlSalts[url][NEXT],getRandomSeed())
        self.save()
    def genPass(self,url,current = True):
        salt = self.getSalt(url, current)
        return generatePassword(url, self.rndSeed, salt)


def getUser(number):
    """ Find user in database

    Params:
        number: hashed phonenumber

    Returns:
        User object or None

    """
    return User.query.filter(User.phoneNumber == str(number)).first()  

def newUser(number):
    """ Create new users if does not already exist

    Params:
        number: hashed phone number
    
    Returns:
        New user object or None if user already exists

    """
    if userExists(number):
        return None
    user =  User(phoneNumber=number, rndSeed=getRandomSeed(), oneTimeKey=INVALID_KEY, urlSalts={})
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
