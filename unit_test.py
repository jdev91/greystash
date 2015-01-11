import unittest
import json
import string
import re
import random
import time
from flask import session
from app import *


class TestApp(unittest.TestCase):
    def setup(self):
        pass
    def Atest_crypt_hashVal(self):
        for i in range(10):
            testStr = rndString()
            hashedStr = hashVal(testStr)
            print("Test String: " + str(testStr))
            self.assertTrue(isinstance(hashedStr,str))
            self.assertTrue(re.match(r"[^aeiou]+",hashedStr))
    def Atest_crypt_checkMatch(self):
        for i in range(10):
            testStr = rndString()
            hashedStr = hashVal(testStr)
            print("Test String: " + testStr + " - " + hashedStr)
            self.assertTrue(checkMatch(testStr,hashedStr))
    def Atest_user_newUser(self):
        #use the time to guarentee always have a new user
        curTime = hashVal(int(time.time()))
        print("Current time: " + str(curTime))
        user = newUser(curTime)
        self.assertTrue(user != None)
        user = newUser(curTime)
        self.assertTrue(user == None)
    def Atest_user_updateCode(self):
        user = getUser(hashVal(5039271017))
        code = user.updateCode()
        self.assertTrue(code == user.oneTimeKey)
    def Atest_user_checkCode(self):
        user = getUser(hashVal("5039271017"))
        code = user.updateCode()
        self.assertTrue(user.checkCode(code))
        self.assertFalse(user.checkCode(code))
        self.assertFalse(user.checkCode(-1))
    def Atest_get_user(self):
        isUser = getUser(hashVal("5039271017"))
        notUser = getUser(hashVal("99999999999999999999999999999999"))
        self.assertTrue(isUser != None)
        self.assertTrue(notUser == None)
    def Atest_getSalt(self):
        isUser = getUser(hashVal("5039271017"))
        curSalt = isUser.getSalt("facebook.com",True)
        nextSalt = isUser.getSalt("facebook.com", False)
        isUser.updateSalt("facebook.com")
        newSalt = isUser.getSalt("facebook.com", False)
        nextSalt2 =isUser.getSalt("facebook.com", True)
        for salt in [curSalt,nextSalt,nextSalt2,newSalt]:
            print("\tSalt: " + str(salt))
        
        self.assertFalse(curSalt == nextSalt)
        self.assertTrue(nextSalt == nextSalt2)
        self.assertTrue(newSalt != curSalt and newSalt != nextSalt2)
    def Atest_views_login(self):
        with app.test_client() as c:
            retVal = c.post('/login',data=dict(
                number="5039271017"
            ),follow_redirects=True)
    def test_views_genCode(self):
        #with app.test_client() as c:
           # retVal = c.post("/genCode/5039271017")
        pass
    def Atest_generatePassword(self):
        uniqueID = rndString()
        urls = ["https://facebook.com","facebook.com/","https://facebook.com/main/I/wonder/if./this/matters"]
        password = generatePassword("facebook.com",uniqueID,"foo")
        passwordFalse = generatePassword("facebook.com",uniqueID,"")
        self.assertFalse(password == passwordFalse)

        for url in urls:
            passwordNewUrl = generatePassword(url, uniqueID,"foo")
            self.assertTrue(password == passwordNewUrl)
        for i in range(0,100):
            password = generatePassword("foo.com", rndString(), "a")
            print("RND password" +  password)
            self.assertTrue(re.match(PASSWORD_RE, password) or password == None)


    def test_apiCalls(self):
        printUsers()
        user = getUser(hashVal("5039271017"))
        notUser = getUser(hashVal(time.time()))
        with app.test_client() as c:
            #generate current password
            code = str(user.updateCode())
            urlPass = "/api/5039271017/" + code +"/facebookcom"
            password = sendReq(urlPass, c)
            print("Current Password: " + str(password))
            printUsers()
            
            #generate next password
            user = getUser(hashVal("5039271017"))
            code = str(user.updateCode())
            print(code)
            urlNewPass = "/api/new/5039271017/" + code + "/facebookcom"
            password2 = sendReq(urlNewPass,c)
            print("New Password: " + password2)

            self.assertFalse(password == password2)

            #check if url is stale
            urlStale = "/api/isStale/5039271017/facebookcom"
            val = sendReq(urlStale, c)
            print("Staleness: " + val)
            staleness = re.search(r'^T',sendReq(urlStale,c), re.I)
            self.assertTrue(staleness != None)

            #mark website as safe to update
            user = getUser(hashVal("5039271017"))
            code = str(user.updateCode())
            url = "/api/update/5039271017/facebookcom/" + code
            response = sendReq(url, c)
            print("Update status: " + response)
            
            user = getUser(hashVal("5039271017"))
            code = str(user.updateCode())
            urlPass = "/api/5039271017/" + code +"/facebookcom"
            password3 = sendReq(urlPass, c)
            user = getUser(hashVal("5039271017"))
            code = str(user.updateCode())
            print(code)
            urlNewPass = "/api/new/5039271017/" + code + "/facebookcom"
            password4 = sendReq(urlNewPass, c)
            for i in [password, password2, password3, password4]:
                print(i)

            self.assertTrue(password3 == password2)
            self.assertTrue(password4 != password3)

             

def printUsers():
    users = User.query.all()
    for u in users:
        print(str(u) + "\n")


def sendReq(url,c):
    return json.loads(c.get(url).data)["msg"]



def rndString():
    return "".join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for i in range(12))

if __name__ == '__main__':
    unittest.main()
