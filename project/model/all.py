from project.database import db, Base, ma
import datetime
from sqlalchemy import ForeignKey
customer_plan_junction = db.table('customer_plan_junction', 
    db.column('customer_id', db.foreignkey('customer.id')),
    db.column('plan_id', db.foreignkey('plan.id'))
)

class Auction(Base):
    __tablename__ = 'auction'
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_date = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    start_date = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    end_date = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    minimum_price_increment = db.Column(db.DECIMAL(precision=20, scale=4), nullable=False)
    items = db.relationship('Item')
    plan_id = db.Column(db.BigInteger, db.ForeignKey('plan.id'))
class Address(Base):
    __tablename__ = 'address'
    id = db.Column(db.BigInteger, primary_key=True)
    country = db.Column(db.String(length=25), nullable=False)
    city = db.Column(db.String(length=30), nullable=False)
    phone_number = db.Column(db.String(length=25), nullable=False)
    address = db.Column(db.String(length=255), nullable=False)
    postal_code = db.Column(db.String(length=30), nullable=False)







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

    


insurance_item_junction = db.Table('insurance_item_junction',
    db.Column('insurance_id', db.ForeignKey('insurance.id')),
    db.Column('item_id', db.ForeignKey('item.id'))
)


class Insurance(Base):
    __tablename__ = "insurance"
    id = db.Column(db.BigInteger, primary_key=True)
    company_name = db.Column(db.String(length=100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.DECIMAL(precision=20, scale=4), nullable=False)
    items = db.relationship('Item', secondary='insurance_item_junction', back_populates='insurances')
    # insurance_serial = Column(String(100))



class Item(Base):
    __tablename__ = 'item'
    id = db.Column(db.BigInteger, primary_key=True)
    price = db.Column(db.DECIMAL(precision=20, scale=4), nullable=True)
    off = db.Column(db.DECIMAL(precision=20, scale=4), default=0)
    made_in = db.Column(db.String(length=25))
    auction_id = db.Column(db.BigInteger, db.ForeignKey('auction.id'))
    product_id = db.Column(db.BigInteger, db.ForeignKey('product.id'))
    offers = db.relationship('Offer')
    store_id = db.Column(db.BigInteger, db.ForeignKey('store.id'))
    insurances = db.relationship('Insurance', secondary='insurance_item_junction', back_populates='items')




manufacture_product_junction = db.Table('manufacture_product_junction',
    db.Column('manufacture_id', db.ForeignKey('manufacture.id')),
    db.Column('product_id', db.ForeignKey('product.id'))
)



class Manufacture(Base):
    __tablename__ = 'manufacture'
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(length=25), nullable=False)
    review = db.Column(db.Text, nullable=True)
    details =  db.Column(db.PickleType, nullable=True)
    products = db.relationship('Product', secondary='manufacture_product_junction', back_populates='manufactures')




class Offer(Base):
    __tablename__ = 'offer'
    id = db.Column(db.BigInteger, primary_key=True)
    offer_price = db.Column(db.DECIMAL(precision=20, scale=4), nullable=False)
    date = db.Column(db.TIMESTAMP, default=datetime.datetime.now)
    order_id = db.Column(db.BigInteger, db.ForeignKey('order.id'))
    item_id = db.Column(db.BigInteger, db.ForeignKey('item.id'))



class Order(Base):

    __tablename__ = 'order'
 
    id = db.Column(db.BigInteger, primary_key=True)
    create_date = db.Column(db.TIMESTAMP, default=datetime.datetime.now)
    modify_date = db.Column(db.TIMESTAMP, default=datetime.datetime.now)
    custormer_id = db.Column(db.BigInteger, db.ForeignKey('customer.id'))
    offers = db.relationship('Offer')
    shipments = db.relationship('Shipment')




class Payment(Base):
    __tablename__ = 'payment'
    id = db.Column(db.BigInteger, primary_key=True)
    amount = db.Column(db.DECIMAL(precision=20, scale=4), nullable=False)
    payment_id = db.Column(db.String(length=25))
    date = db.Column(db.TIMESTAMP, default=datetime.datetime.now)
    customer_id = db.Column(db.BigInteger, db.ForeignKey('customer.id'))

    



class Plan(Base):
    __tablename__ = 'plan'

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(length=100), nullable=False)
    price = db.Column(db.DECIMAL(precision=20, scale=4), nullable=True)
    total_bids = db.Column(db.Integer, default=0)
    auctions = db.relationship('Auction')
    customers = db.relationship('Customer', secondary='customer_plan_junction', back_populates='plans')



class Product(Base):

    __tablename__ = 'product'
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(length=25), nullable=False)
    total_available = db.Column(db.Integer, nullable=False)
    review = db.Column(db.Text)
    stars = db.Column(db.Integer, default=0)
    details =  db.Column(db.PickleType, nullable=True)
    items = db.relationship('Item')
    category_id = db.Column(db.BigInteger, db.ForeignKey('category.id'))
    comments = db.relationship("Comment")
    # state = Column("String", )sadasd
    manufactures = db.relationship('Manufacture', secondary='manufacture_product_junction', back_populates='products')

    


class Role(Base):
    __tablename__ = 'role'
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(512))
    customer_id = db.Column(db.BigInteger, db.ForeignKey('customer.id'))




class Shipment(Base):
    __tablename__ = 'shipment'
    id = db.Column(db.BigInteger, primary_key=True)
    transport_company = db.Column(db.String(length=100), nullable=False)    
    transport_method = db.Column(db.String(length=100), nullable=False)
    send_date = db.Column(db.TIMESTAMP, default=datetime.datetime.now)
    recieve_date = db.Column(db.TIMESTAMP, default=datetime.datetime.now)
    price = db.Column(db.DECIMAL(precision=20, scale=4), nullable=False)
    transport_vehicle = db.Column(db.String(length=35), nullable=True)
    order_id = db.Column(db.BigInteger, db.ForeignKey('order.id'))
    insurance_id = db.Column(db.BigInteger, db.ForeignKey('insurance.id'))




class Store(Base):
    __tablename__ = 'store'

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(length=25), nullable=True)
    desciption = db.Column(db.String(length=255), nullable=True)
    items = db.relationship('Item') 
    address_id = db.Column(db.BigInteger, db.ForeignKey('address.id'))

class Comment(Base):
    __tablename__ = 'comment'
    id = db.Column(db.BigInteger, primary_key=True)
    title = db.Column(db.String(length=255), nullable=False)
    message = db.Column(db.String(length=2048), nullable=False)
    stars = db.Column(db.Integer, default=0)
    customer_id = db.Column(db.BigInteger, db.ForeignKey('customer.id'))
    product_id = db.Column(db.BigInteger, db.ForeignKey('product.id'))
    

class CommentSchema(ma.ModelSchema):
    class Meta:
        model = Comment 


class StoreSchema(ma.ModelSchema):
    class Meta:
        model = Store 




class ItemSchema(ma.ModelSchema):
    class Meta:
        model = Item



class AddressSchema(ma.ModelSchema):
    class Meta:
        model = Address 


class AuctionSchema(ma.ModelSchema):
    class Meta:
        model = Auction 



class CustomerSchema(ma.ModelSchema):
    class Meta:
        model = Customer


class InsuranceSchema(ma.ModelSchema):
    class Meta:
        model = Insurance 

class ManufactureSchema(ma.ModelSchema):
    class Meta:
        model = Manufacture 
class OfferSchema(ma.ModelSchema):
    class Meta:
        model = Offer 
class OrderSchema(ma.ModelSchema):
    class Meta:
        model = Order 
class PaymentSchema(ma.ModelSchema):
    class Meta:
        model = Payment 

class PlanSchema(ma.ModelSchema):
    class Meta:
        model = Plan 

class ProductSchema(ma.ModelSchema):
    class Meta:
        model = Product 
class RoleSchema(ma.ModelSchema):
    class Meta:
        model = Role 

class ShipmentSchema(ma.ModelSchema):
    class Meta:
        model = Shipment 