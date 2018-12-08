from .melipayamak import SMS_Api
from definitions import SMS_USERNAME,SMS_PASSWORD,SMS_SERVICE_NUMBER


def SendSMS(mobile,message):
    print "sending sms to ",mobile
    sms_api = SMS_Api(SMS_USERNAME,SMS_PASSWORD)
    sms = sms_api.sms()
    resp = sms.send(mobile ,SMS_SERVICE_NUMBER,message)
    print "response",resp
    result = {"status_code":resp['Value']}
    if resp['RetStatus'] == 1 and len(resp['Value'])>15 and resp['StrRetStatus']== 'Ok' :
        result["success"] = True
    else:
        result["success"] = False
    return result

def SendSMSForce(mobile,text,bodyId):
    print "send force sms to ",mobile
    sms_api = SMS_Api(SMS_USERNAME,SMS_PASSWORD)
    sms = sms_api.sms()
    resp = sms.send_force(SMS_SERVICE_NUMBER,mobile, text, bodyId)
    print "response",resp
    result = {"status_code":resp['Value']}

    if resp['RetStatus'] == 1 and len(resp['Value'])>15 and resp['StrRetStatus']== 'Ok' :
        result["success"] = True
    else:
        result["success"] = False
    return result
