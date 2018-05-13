# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from ..database import db
from .. import app
from ..model import *
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from ..model.advertisement import Advertisement
from ..model.event import Event
from .upload import *


# Create admin
admin = Admin(
    app,
    " بید بازی ",
    base_template='admin.html',
    template_mode='bootstrap3',
)
#admin.add_view(MyView(name='My View', menu_icon_type='glyph', menu_icon_value='glyphicon-home'))
admin.add_view(AvatarUpload(User, db.session))
admin.add_view(CategoryUpload(Category, db.session))
admin.add_view(ProductUpload(Product, db.session))
admin.add_view(ModelView(Auction, db.session))
admin.add_view(ModelView(Address, db.session))
admin.add_view(ModelView(Gift, db.session))
admin.add_view(ModelView(Insurance, db.session))
admin.add_view(ModelView(Inventory, db.session))
admin.add_view(ModelView(Manufacture, db.session))
admin.add_view(ModelView(Offer, db.session))
admin.add_view(ModelView(Item, db.session))
admin.add_view(ModelView(Event, db.session))
admin.add_view(ModelView(Plan, db.session))
admin.add_view(AdvertisementUpload(Advertisement, db.session))
