import unittest
import string
import re
import random
from app import *

class TestApp(unittest.TestCase):
    def setup(self):
        app.run(debug = True)
    
    def test_crypt_hashVal(self):
        for i in range(10):
            testStr = rndString()
            hasedStr = hashVal(testStr)
            print("Test String: " + str(testStr))
            self.assertTrue(isinstace(hashedStr,str))
            self.assertTrue(re.match(r"[^aeiou]+",hashedStr))
def rndString():
    return "".join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for i in range(12))

if __name__ == '__main__':
    unittest.main()
