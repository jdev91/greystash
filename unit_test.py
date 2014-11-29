import unittest
import string
import re
import random
import time
from flask import session
from app import *

class TestApp(unittest.TestCase):
    def setup(self):
        pass
    def test_crypt_hashVal(self):
        for i in range(10):
            testStr = rndString()
            hashedStr = hashVal(testStr)
            print("Test String: " + str(testStr))
            self.assertTrue(isinstance(hashedStr,str))
            self.assertTrue(re.match(r"[^aeiou]+",hashedStr))
    def test_crypt_checkMatch(self):
        for i in range(10):
            testStr = rndString()
            hashedStr = hashVal(testStr)
            print("Test String: " + testStr + " - " + hashedStr)
            self.assertTrue(checkMatch(testStr,hashedStr))
    def test_user_newUser(self):
        #use the time to guarentee always have a new user
        curTime = hashVal(int(time.time()))
        print("Current time: " + str(curTime))
        user = newUser(curTime)
        self.assertTrue(user != None)
        user = newUser(curTime)
        self.assertTrue(user == None)
    def test_views_login(self):
        with app.test_client() as c:
            retVal = c.post('/login',data=dict(
                number="5039271017"
            ),follow_redirects=True)
            self.assertTrue(session["USER"] != None)
            print(str(retVal))
            retVal = c.post('/logout')
            print(str(retVal))
            self.assertTrue(session["USER"] == None)
def rndString():
    return "".join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for i in range(12))

if __name__ == '__main__':
    unittest.main()
