from .melipayamak import SMS_Api
from definitions import SMS_USERNAME,SMS_PASSWORD,SMS_SERVICE_NUMBER

sms_api = SMS_Api(SMS_USERNAME,SMS_PASSWORD)
sms = sms_api.sms()

def SendSMS(mobile,message):
    response = sms.send(mobile ,SMS_SERVICE_NUMBER,message)
    if response['RetStatus'] == 1 and response['StrRetStatus']== 'Ok' :
        return True
    return False
