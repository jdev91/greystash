import sys, traceback
from app import *
from flask.ext.mail import Mail, Message

carierTypes = ["@txt.att.net"]
carierTypes_full = ["@message.alltel.com", "@txt.att.net", "@myboostmobile.com",
        "@messaging.nextel", "@messaging.sprintpcs.com", "@tmomail.net",
        "@email.uscc.net", "@vtext.com", "@vmobl.com"]

def sendMsg(recipient,text):

    msg = Message("One Time code.", sender= app.config["MAIL_USERNAME"],recipients = [recipient])
    msg.body = text
    mail.send(msg)
def sendCode(number,code):
    """ Send confirmation code to user

    Params:
        number (int): phonenumber to send to 
        code (int): code stored in the database
    
    Return:
        None

    """
    print("Number: " + str(number) + " Code: " + str(code))
    #not sure what provide they have, but number can only be on one
    for carierType in carierTypes:
        print("Sending message to " + carierType)
        sendMsg(str(number) + carierType, str(code))

