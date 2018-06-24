# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from flask_restful import Resource
from PyMellat.PyMellat import BMLPaymentAPI
from flask_login import login_required, current_user
from flask import make_response, jsonify, url_for, request, render_template ,redirect
from definitions import BANK_MELLAT_PASSWORD, BANK_MELLAT_TERMINAL_ID, BANK_MELLAT_USERNAME
import random
from ..model.payment import *
from ..model.order import *
from ..model.user import *
import time

'''
# Request Payment Token:
bml = BMLPaymentAPI('username', 'password', long(TerminalID))
pay_token = bml.request_pay_ref(saved_random_number, price, call_back_address, extra_data)

# Verify Payment :
# When payment is done by user, user returns to call_back_address with POST method.
# POST parameters : RefId, ResCode, SaleOrderId, SaleReferenceId

bml = BMLPaymentAPI(bank_username, bank_password, terminal_id)
verify_res = bml.verify_payment(long(SaleOrderId), long(SaleReferenceId))

# Settle Request:
# If every thing was OK and verify_res[0] == '0' :
bml.settle_payment(long(SaleOrderId), SaleReferenceId)
'''

class MellatGatewayCallBack(Resource):
    def post(self):
        print request.form
        print "mellat callback"
        data = request.form
        ref_id = data['RefId']
        res_code = data['ResCode']
        sale_order_id = data['SaleOrderId']
        sale_refrence_id = data['SaleReferenceId']
        bml = BMLPaymentAPI(BANK_MELLAT_USERNAME, BANK_MELLAT_PASSWORD, BANK_MELLAT_TERMINAL_ID)
        verify_res = bml.verify_payment(sale_order_id,sale_refrence_id)

        print ref_id
        print res_code
        print sale_order_id
        print sale_refrence_id
        print verify_res

        payment = Payment.query.filter_by(GUID=sale_order_id,ref_id=ref_id).first()
        payment.sale_order_id = str(sale_order_id)

        if verify_res[1] == '0':
            payment.status = PaymentStatus.PAID
            payment.sale_refrence_id = str(sale_refrence_id)
            bml.settle_payment(sale_order_id , sale_refrence_id)
        else:
            payment.status = PaymentStatus.ERROR

        db.session.add(payment)
        db.session.commit()

        return redirect('/callback/payment/'+str(payment.id))

        # return make_response(jsonify({"success": True, "message": {"success": "پرداخت با موفقیت انجام شد"}}), 200)
        # return make_response(jsonify({"success": False, "message": {"error": "پرداخت با خطا مواجه شد"}}), 400)



class MellatGateway(Resource):
    @login_required
    def post(self):
        # current_user = User.query.filter_by(username="mohammad").first()
        # if not request.is_json:
        #     return make_response(jsonify({"message": {"error": "not json"}}, 400))
        pid = request.form.get('pid')
        payment = Payment.query.get(pid)
        bml = BMLPaymentAPI(BANK_MELLAT_USERNAME, BANK_MELLAT_PASSWORD, BANK_MELLAT_TERMINAL_ID)
        payment.GUID = int(time.time())
        pay_token = bml.request_pay_ref( payment.GUID, int(payment.amount) * 10, "http://bidbazi.ir/api/user/mellat/callback", "درگاه پرداخت بیدبازی")
        payment.ref_id = pay_token
        db.session.add(payment)
        db.session.commit()
        print pay_token
        if pay_token:
            return make_response(jsonify({'success':True,"ref_id": pay_token}), 200)
        else:
            return make_response(jsonify({'success':False,"pay_token":pay_token,"message":"خطای بانک"}),400)
