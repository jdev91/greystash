import  binascii
import re
from string import maketrans
from passlib.hash import pbkdf2_sha256
PASSWORD_RE = r'^(?=.{8,}$)(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.*[\^\-*#~!@$%&()_+=`]).*'
PASSWORD_LENGTH = 16
def checkMatch(origVal, storedVal):
    """Confirms if an unhashed value matches a stored value

    Args:
        origVal (str): unhashed value
        storedVal (str): hashed value

    Returns:
        True if values match, False otherwise

    """
    match = False
    if hashVal(origVal) == storedVal:
        match = True
    return match

def hashVal(value):
    """ Converts parameter to hashed version

    None:
        Converts parameter to a string before hashing

    Args:
        value: variable to hash

    Returns:
        Hahsed string

    """
    password = pbkdf2_sha256.encrypt(str(value),salt=b'')
    password = re.sub(r'.*\$',"",password)#only care about the checksum
    password = password.translate(maketrans("aeiou","!@#$%"))
    return password 

def generatePassword(url, uniqueID, salt):
    
    input = canonicalURL(url) + str(uniqueID) +str(salt)
    for i in range(0,200000):
        password = hashVal(input)[:PASSWORD_LENGTH]
        if re.match(PASSWORD_RE, password):
            return password
        input = password
    return None
def canonicalURL(url):
    #convert to canonical URL
    for regex in [r'https?://', r"www\.", r"/.*"]:
        url = re.sub(regex,"",url)
        print("\t URL: "  + url)
    match = re.search(r'.*?\.?(.*\..*)', url)
    if match:
        url = match.group(1)
    print("Canonical URL: " + url)
    return url
