# auction

### how to use marshmallow:
create schema table for each model cointaining the field that you want to expose when dumping the model. 
if the field in Nested and you don't need some fields of the other object to be dumped add them to `exclude = tuple()` parameter:
  example: `payments = fields.Nested('PaymentSchema', many=True, exclude=('amount',))`
  
 ### authentication:
 for those routes which they need authentication, just annotation them with `@jwt_required`.
