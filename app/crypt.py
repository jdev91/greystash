import  binascii
import re
from string import maketrans
from passlib.hash import pbkdf2_sha256

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

