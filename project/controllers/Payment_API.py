# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from flask_restful import Resource
from Payment.PyMellat import BMLPaymentAPI
from Payment.Zarinpal import ZarinpalPaymentAPI
from flask_login import login_required, current_user
from flask import make_response, jsonify, url_for, request, render_template ,redirect
from definitions import BANK_MELLAT_PASSWORD, BANK_MELLAT_TERMINAL_ID, BANK_MELLAT_USERNAME
import random
from ..model.payment import *
from ..model.order import *
from ..model.user import *
import time
from flask_jwt_extended import jwt_required, jwt_refresh_token_required, fresh_jwt_required

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
        print "mellat callback"
        print request.form
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
    @jwt_required
    def post(self):
        # current_user = User.query.filter_by(username="mohammad").first()
        # if not request.is_json:
        #     return make_response(jsonify({"message": {"error": "not json"}}, 400))
        pid = request.form.get('pid')
        payment = Payment.query.get(pid)
        bml = BMLPaymentAPI(BANK_MELLAT_USERNAME, BANK_MELLAT_PASSWORD, BANK_MELLAT_TERMINAL_ID)
        pay_token = bml.request_pay_ref( payment.GUID, int(payment.amount) * 10, "http://unibid.ir/api/user/mellat/callback", "درگاه پرداخت یونی بید")
        payment.ref_id = pay_token
        db.session.add(payment)
        db.session.commit()
        print pay_token
        if pay_token:
            return make_response(jsonify({'success':True,"ref_id": pay_token}), 200)
        else:
            return make_response(jsonify({'success':False,"pay_token":pay_token,"message":"خطای بانک"}),400)

class ZarinpalGateway(Resource):
    @jwt_required
    def post(self):
        data = request.get_json(force=True)
        pid = int(data.get("pid", None))
        payment = Payment.query.get(pid)
        orders = Order.query.filter_by(payment_id = pid).all()
        for order in orders:
            order.status = OrderStatus.DEACTIVATE
            db.session.add(order)
            db.session.commit()

        zpl = ZarinpalPaymentAPI()
        pay_token = zpl.send_request(int(payment.amount),current_user.email,current_user.mobile,"http://unibid.ir/api/user/zarinpal/gateway/callback" ,"درگاه پرداخت یونی بید")
        payment.ref_id = pay_token.Authority
        payment.status = PaymentStatus.BANK
        db.session.add(payment)
        db.session.commit()
        print 'pid',pid,'token',pay_token
        if pay_token.Status==100:
            return make_response(jsonify({'success':True,"ref_id": pay_token.Authority}), 200)
        else:
            return make_response(jsonify({'success':False,"ref_id": pay_token.Authority,"message":"خطای پرداخت"}),400)


class ZarinpalGatewayCallback(Resource):
    def get(self):
        status = request.args.get('Status')
        authority = request.args.get('Authority')

        payment = Payment.query.filter_by(ref_id=authority).first()

        zpl = ZarinpalPaymentAPI()
        verify_res = zpl.verify(status,authority,payment.amount)
        print 'verify_res',verify_res
        if verify_res == 100:
            payment.status = PaymentStatus.PAID
        elif(verify_res == -21 or verify_res == -22):
            payment.status = PaymentStatus.ABORT
        else:
            payment.status = PaymentStatus.UNPAID

        db.session.add(payment)
        db.session.commit()

        return redirect('/callback/payment/'+str(payment.id))
