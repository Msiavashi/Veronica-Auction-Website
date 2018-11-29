from .melipayamak import SMS_Api
from definitions import SMS_USERNAME,SMS_PASSWORD,SMS_SERVICE_NUMBER

def SendSMS(mobile,message):
    print "sending sms to ",mobile
    sms_api = SMS_Api(SMS_USERNAME,SMS_PASSWORD)
    sms = sms_api.sms()
    response = sms.send(mobile ,SMS_SERVICE_NUMBER,message)
    print "send sms response :" ,response['Value']
    if response['Value'] == 1 and response['StrRetStatus']== 'Ok' :
        return True
    return False
