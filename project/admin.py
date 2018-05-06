from .database import db
from project import app
from project.model import *
from project.model.advertisement import Advertisement

import os
from flask import url_for, redirect, render_template, request, abort

from flask_security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required, current_user
from flask_security.utils import encrypt_password
from flask_admin import Admin
from flask_admin import helpers as admin_helpers
from flask_admin.contrib.sqla import ModelView


# Create admin
admin = Admin(
    app,
    " بید بازی ",
    base_template='admin.html',
    template_mode='bootstrap3',
)

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Category, db.session))
admin.add_view(ModelView(Product, db.session))
admin.add_view(ModelView(Auction, db.session))
admin.add_view(ModelView(Address, db.session))
admin.add_view(ModelView(Gift, db.session))
admin.add_view(ModelView(Insurance, db.session))
admin.add_view(ModelView(Inventory, db.session))
admin.add_view(ModelView(Manufacture, db.session))
admin.add_view(ModelView(Offer, db.session))
admin.add_view(ModelView(Item, db.session))
admin.add_view(ModelView(Advertisement, db.session))
