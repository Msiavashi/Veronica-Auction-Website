import datetime
from project.database import Base, db, ma
# from project.model.role import Role
# from project.model.comment import Comment
# from project.model.address import Address
# from project.model.payment import Payment
# from project.model.order import Order 
# from project.model.customer_plan_junction import customer_plan_junction
# from project.model.plan import Plan
from project.database import ma

class Customer(Base):
    __tablename__ = 'customer'
    id = db.Column(db.BigInteger, primary_key=True)
    first_name = db.Column(db.String(length=50), nullable=False)
    last_name = db.Column(db.String(length=50), nullable=False)
    username = db.Column(db.String(length=30), nullable=False)
    password = db.Column(db.String(length=30), nullable=False)
    register_date = db.Column(db.TIMESTAMP, default=datetime.datetime.now)
    phone_number = db.Column(db.String(length=25), nullable=False)
    email = db.Column(db.String(length=100))
    credit = db.Column(db.DECIMAL(precision=20, scale=4), default=0)
    gift_credit = db.Column(db.DECIMAL(precision=20, scale=4), default=0)
    organization_or_person = db.Column(db.String(length=20), nullable=False)
    roles = db.relationship('Role')
    comments = db.relationship('Comment')
    address_id = db.Column(db.BigInteger, db.ForeignKey('address.id'))
    payments = db.relationship('Payment')
    orders = db.relationship('Order')
    plans = db.relationship('Plan', secondary='customer_plan_junction', back_populates='customers', lazy='subquery')

class CustomerSchema(ma.ModelSchema):
    class Meta:
        model = Customer
    