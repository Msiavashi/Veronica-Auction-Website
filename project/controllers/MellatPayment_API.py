from flask_restful import Resource
from PyMellat.PyMellat import BMLPaymentAPI
from flask_login import login_required, current_user
from flask import make_response, jsonify, url_for, request, render_template
from definitions import BANK_MELLAT_PASSWORD, BANK_MELLAT_TERMINAL_ID, BANK_MELLAT_USERNAME
import random
from ..model.payment import *
from ..model.order import *

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
        data = request.data.get_json(force=True)
        ref_id = data['RefId']
        res_code = data['ResCode']
        sale_order_id = data['SaleOrderId']
        sale_refrence_id = data['SaleReferenceId']
        bml = BMLPaymentAPI(BANK_MELLAT_USERNAME, BANK_MELLAT_PASSWORD, long(BANK_MELLAT_TERMINAL_ID))
        verify_res = bml.verify_payment(long(sale_order_id), long(sale_refrence_id)) 

        if verify_res[0] == '0':
            payment = Payment.query.get(request.args.get('pid'))
            payment.status = PaymentStatus.PAID
            payment.ref_id = ref_id
            payment.sale_order_id = sale_order_id
            payment.sale_refrence_id = sale_refrence_id
            for order in payment.orders:
                order.status = OrderStatus.PAID
                
            db.session.add(payment)
            db.session.commit()


            bml.settle_payment(long(sale_order_id), sale_refrence_id)
            return make_response(jsonify({"success": True, "message": {"success": "پرداخت با موفقیت انجام شد"}}), 200)
        return make_response(jsonify({"success": False, "message": {"error": "پرداخت با خطا مواجه شد"}}), 400)
        


class MellatGateway(Resource):

    @login_required
    def post(self, uid, pid):
        if not request.data.is_json:
            return make_response(jsonify({"message": {"error": "not json"}}, 400))
        data = request.data.get_json(force=True)
        bml = BMLPaymentAPI(BANK_MELLAT_USERNAME, BANK_MELLAT_PASSWORD, long(BANK_MELLAT_TERMINAL_ID))
        price = data['price']
        pay_token = bml.request_pay_ref(current_user.id, price, url_for('mellatgatewaycallback', uid=current_user.id, pid=pid), None)
        if pay_token:
            return make_response(jsonify({"pay_token": pay_token}), 200)
        else:
            return make_response(jsonify({"message": {"error": "خطای بانک"}}), 400)
        


