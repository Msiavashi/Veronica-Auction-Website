from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from db_config import Config

engine = create_engine('mysql://' + Config.username + ':' + Config.password + '@' + Config.host_name + ':' + Config.port + '/' + Config.db_name, pool_recycle=3600, convert_unicode=True)

db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    from model.auction import Auction
    from model.address import Address
    from model.category import Category 
    from model.category_product_junction import category_product_junction
    from model.comment import Comment 
    from model.customer import Customer 
    from model.customer_plan_junction import customer_plan_junction
    from model.insurance import Insurance 
    from model.insurance_item_junction import insurance_item_junction
    from model.item import Item 
    from model.manufacture import Manufacture 
    from model.manufacture_product_junction import manufacture_product_junction
    from model.offer import Offer
    from model.order import Order 
    from model.payment import Payment 
    from model.plan import Plan 
    from model.product import Product 
    from model.role import Role 
    from model.shipment import Shipment 
    from model.store import Store 

    Base.metadata.create_all(bind=engine)

# print "initing..."
init_db()
# print "done"