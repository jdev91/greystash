import  binascii, hashlib

def checkMatch(origVal, storedVal):
    match = False
    if hashVal(origVal) == storedVal:
        match = True
    return match

def hashVal(value):
    dk = hashlib.pbkdf2_hmac('sha256',value,b'',100000,600)
    hashedPass = binascii.b2a_base64(dk)
    hashPass = hashedPass.translate(hashedPass.maketrans("aeiou","!@#$%"))
    return hashPass

