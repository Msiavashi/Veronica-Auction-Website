from project import ma
from project.model.user import User
from project.model.payment_schema import PaymentSchema
from marshmallow import fields
class UserSchema(ma.Schema):
    payments = fields.Nested('PaymentSchema', many=True, exclude=('user_id'))
    class Meta:
        # model = User
        fields = ('id', 'username', 'password', 'payments')
        
