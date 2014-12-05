from app import *
import smtplib

USER_NAME =  "theonetheycallthestash@gmail.com"
USER_PASSWORD = "ljmj2310"
MAIL_SERVER = 'smtp.gmail.com:587'
carierTypes = ["@message.alltel.com", "@txt.att.net", "@myboostmobile.com",
        "@messaging.nextel", "@messaging.sprintpcs.com", "@tmomail.net",
        "@email.uscc.net", "@vtext.com", "@vmobl.com"]

def sendMsg(recipient,text):
    server = smtplib.SMTP(MAIL_SERVER)
    try:
        server.starttls()
        server.login(USER_NAME, USER_PASSWORD)
        server.sendmail(USER_NAME, str(recipient), str(text))
    except:
        pass
    server.quit()
def sendCode(code, number):
    """ Send confirmation code to user

    Params:
        code (int): code stored in the database
        number (int): phonenumber to send to 
    
    Return:
        None

    """
    #not sure what provide they have, but number can only be on one
    for carierType in carierTypes:
        sendMsg(str(number) + carierType, str(code))

