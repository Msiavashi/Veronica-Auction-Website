# -*- coding: utf-8 -*-
import sys
from importlib import reload
reload(sys)
# sys.setdefaultencoding("utf-8")

from ..database import db
from .. import app
from ..model import *
from .upload import *
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

# Create admin
admin = Admin(
    app,
    " بید بازی ",
    base_template='admin.html',
    template_mode='bootstrap3',
)
#admin.add_view(MyView(name='My View', menu_icon_type='glyph', menu_icon_value='glyphicon-home'))
admin.add_view(AvatarUpload(User, db.session,name='کاربران',menu_icon_type='fa', menu_icon_value='fa fa-user'))
admin.add_view(ModelView(Role, db.session,name='نقش',menu_icon_type='fa', menu_icon_value='fa fa-group'))
admin.add_view(CategoryUpload(Category, db.session,name='دسته بندی',menu_icon_type='fa', menu_icon_value='fa fa-user'))
admin.add_view(ModelView(Product, db.session,name='محصولات',menu_icon_type='fa', menu_icon_value='fa fa-user'))
admin.add_view(ModelView(Auction, db.session,name='حراجی ها',menu_icon_type='fa', menu_icon_value='fa fa-user'))
admin.add_view(ModelView(Address, db.session,name='آدرس ها',menu_icon_type='fa', menu_icon_value='fa fa-user'))
admin.add_view(ModelView(Gift, db.session,name='جایزه ها',menu_icon_type='fa', menu_icon_value='fa fa-user'))
admin.add_view(ModelView(Insurance, db.session,name='بیمه',menu_icon_type='fa', menu_icon_value='fa fa-user'))
admin.add_view(ModelView(Garanty, db.session,name='گارانتی',menu_icon_type='fa', menu_icon_value='fa fa-user'))
admin.add_view(ModelView(Inventory, db.session,name='انبار',menu_icon_type='fa', menu_icon_value='fa fa-user'))
admin.add_view(ModelView(Manufacture, db.session,name='کارخانه ها',menu_icon_type='fa', menu_icon_value='fa fa-user'))
admin.add_view(ModelView(Offer, db.session,name='پیشنهادات',menu_icon_type='fa', menu_icon_value='fa fa-user'))
admin.add_view(ItemImageUpload(Item, db.session,name='آیتم های محصولات',menu_icon_type='fa', menu_icon_value='fa fa-user'))
admin.add_view(ModelView(Event, db.session,name='تخفیف های مناسبتی',menu_icon_type='fa', menu_icon_value='fa fa-user'))
admin.add_view(ModelView(PaymentMethod, db.session,name='روش های پرداخت',menu_icon_type='fa', menu_icon_value='fa fa-user'))
admin.add_view(ModelView(Plan, db.session,name='پلن های پیش فرض',menu_icon_type='fa', menu_icon_value='fa fa-user'))
admin.add_view(ModelView(AuctionPlan, db.session,name='پلن حراجی',menu_icon_type='fa', menu_icon_value='fa fa-user'))
admin.add_view(ModelView(UserPlan, db.session,name='پلن حراجی کاربر',menu_icon_type='fa', menu_icon_value='fa fa-user'))
admin.add_view(ModelView(UserAuctionParticipation, db.session,name='شرکت کنندگان حراجی',menu_icon_type='fa', menu_icon_value='fa fa-user'))
admin.add_view(AdvertisementUpload(Advertisement, db.session,name='تبلیغات',menu_icon_type='fa', menu_icon_value='fa fa-user'))
admin.add_view(ModelView(UserMessage, db.session,name='پیام های کاربران سایت',menu_icon_type='fa', menu_icon_value='fa fa-user'))
admin.add_view(ModelView(GuestMessage, db.session,name='پیام های کاربران مهمان',menu_icon_type='fa', menu_icon_value='fa fa-user'))
