# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from ..database import db
from .. import app
from .classes import *
from ..model import *
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from passlib.hash import pbkdf2_sha256 as sha256

from flask_security import current_user, login_required, Security,SQLAlchemyUserDatastore
# Initialize the SQLAlchemy data store and Flask-Security.
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

# Create admin
admin = Admin(
    app," بیدبازی ",index_view=MyAdminIndexView(),base_template='admin.html',template_mode='bootstrap3',
)

admin.add_view(UserAdmin(User, db.session,name='کاربران',menu_icon_type='fa', menu_icon_value='fa fa-user'))
admin.add_view(RoleAdmin(Role, db.session,name='نقش',menu_icon_type='fa', menu_icon_value='fa fa-user'))
admin.add_view(CategoryAdmin(Category, db.session,name='دسته بندی',menu_icon_type='fa', menu_icon_value='fa fa-user'))
admin.add_view(ProductAdmin(Product, db.session,name='محصولات',menu_icon_type='fa', menu_icon_value='fa fa-user'))
admin.add_view(ItemAdmin(Item, db.session,name='آیتم های محصولات',menu_icon_type='fa', menu_icon_value='fa fa-user'))
admin.add_view(AuctionAdmin(Auction, db.session,name='حراجی ها',menu_icon_type='fa', menu_icon_value='fa fa-user'))
admin.add_view(OfferAdmin(Offer, db.session,name='پیشنهادات',menu_icon_type='fa', menu_icon_value='fa fa-user'))
admin.add_view(OrderAdmin(Order, db.session,name='سفارشات',menu_icon_type='fa', menu_icon_value='fa fa-user'))
admin.add_view(PaymentAdmin(Payment, db.session,name='پرداخت ها',menu_icon_type='fa', menu_icon_value='fa fa-user'))
admin.add_view(ShipmentAdmin(Shipment, db.session,name='ارسال ها',menu_icon_type='fa', menu_icon_value='fa fa-user'))
admin.add_view(PlanAdmin(Plan, db.session,name='پلن های پیش فرض',menu_icon_type='fa', menu_icon_value='fa fa-user'))
admin.add_view(AuctionPlanAdmin(AuctionPlan, db.session,name='پلن حراجی',menu_icon_type='fa', menu_icon_value='fa fa-user'))
admin.add_view(UserPlanAdmin(UserPlan, db.session,name='پلن حراجی کاربر',menu_icon_type='fa', menu_icon_value='fa fa-user'))
admin.add_view(UserAuctionParticipationAdmin(UserAuctionParticipation, db.session,name='شرکت کنندگان حراجی',menu_icon_type='fa', menu_icon_value='fa fa-user'))
admin.add_view(PaymentMethodAdmin(PaymentMethod, db.session,name='روش های پرداخت',menu_icon_type='fa', menu_icon_value='fa fa-user'))
admin.add_view(ShipmentMethodAdmin(ShipmentMethod, db.session,name='روش های ارسال',menu_icon_type='fa', menu_icon_value='fa fa-user'))
admin.add_view(AdvertisementAdmin(Advertisement, db.session,name='تبلیغات',menu_icon_type='fa', menu_icon_value='fa fa-user'))
admin.add_view(EventAdmin(Event, db.session,name='تخفیف های مناسبتی',menu_icon_type='fa', menu_icon_value='fa fa-user'))
admin.add_view(GiftAdmin(Gift, db.session,name='جایزه',menu_icon_type='fa', menu_icon_value='fa fa-user'))
admin.add_view(InsuranceAdmin(Insurance, db.session,name='بیمه',menu_icon_type='fa', menu_icon_value='fa fa-user'))
admin.add_view(GarantyAdmin(Garanty, db.session,name='گارانتی',menu_icon_type='fa', menu_icon_value='fa fa-user'))
admin.add_view(InventoryAdmin(Inventory, db.session,name='انبار',menu_icon_type='fa', menu_icon_value='fa fa-user'))
admin.add_view(ManufactureAdmin(Manufacture, db.session,name='کارخانه ها',menu_icon_type='fa', menu_icon_value='fa fa-user'))
admin.add_view(PaymentMessageAdmin(PaymentMessage, db.session,name='پیام پرداختی های سایت',menu_icon_type='fa', menu_icon_value='fa fa-user'))
admin.add_view(UserMessageAdmin(UserMessage, db.session,name='پیام های کاربران سایت',menu_icon_type='fa', menu_icon_value='fa fa-user'))
admin.add_view(GuestMessageAdmin(GuestMessage, db.session,name='پیام های کاربران مهمان',menu_icon_type='fa', menu_icon_value='fa fa-user'))
admin.add_view(AddressAdmin(Address, db.session,name='آدرس ها',menu_icon_type='fa', menu_icon_value='fa fa-user'))
admin.add_view(StateAdmin(State, db.session,name='استان ها',menu_icon_type='fa', menu_icon_value='fa fa-user'))
