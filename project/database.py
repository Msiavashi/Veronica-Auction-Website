from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from db_config import Config

#engine = create_engine('mysql://' + Config.username + ':' + Config.password + '@' + Config.host_name + ':' + Config.port + '/' + Config.db_name, pool_recycle=3600, convert_unicode=True)
engine = create_engine('postgresql://' + Config.username + ':' + Config.password + '@' + Config.host_name + ':' + Config.port + '/' + Config.db_name)

db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    from model.address import Address
    from model.auction import Auction
    from model.auction_event import AuctionEvent
    from model.category import Category
    from model.comment import Comment
    from model.gift import Gift
    from model.insurance_item import insurance_items
    from model.insurance import Insurance
    from model.inventory import Inventory
    from model.item import Item
    from model.manufacture_product import manufacture_products
    from model.manufacture import Manufacture
    from model.offer import Offer
    from model.order import Order
    from model.payment_item import payment_items
    from model.payment_plan import payment_plans
    from model.payment import Payment
    from model.plan import Plan
    from model.product_event import ProductEvent
    from model.product import Product
    from model.role import Role
    from model.shipment import Shipment
    from model.user_auction import user_auctions
    from model.user_gift import user_gifts
    from model.user_plan import user_plans
    from model.user_product_like import user_product_likes
    from model.user_product_view import user_product_views
    from model.user_role import user_roles
    from model.user import User

    Base.metadata.create_all(bind=engine)

print "initing..."
init_db()
print "done"
