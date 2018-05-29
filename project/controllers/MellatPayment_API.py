from PyMellat.PyMellat import BMLPaymentAPI

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
