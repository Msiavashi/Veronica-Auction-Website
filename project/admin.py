from project.database import db
from project import app
from project.model import *
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from project.model.advertisement import Advertisement
from project.model.event import Event
from project.upload import *


# Create admin
admin = Admin(
    app,
    " بید بازی ",
    base_template='admin.html',
    template_mode='bootstrap3',
)


admin.add_view(ModelView(User, db.session))
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
admin.add_view(AdvertisementUpload(Advertisement, db.session))
admin.add_view(ModelView(Event, db.session))
