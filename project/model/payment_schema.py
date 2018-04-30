from project.model.payment import Payment
from project import ma
from marshmallow import fields

class PaymentSchema(ma.Schema):
    user = fields.Nested('UserSchema', exclude='payments')
    class Meta:
        # model = Payment
        fileds = ('id', 'amount', 'user_id')