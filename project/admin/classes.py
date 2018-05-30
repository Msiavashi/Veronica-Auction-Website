from markupsafe import Markup
from flask import url_for,render_template,abort,session,redirect
from flask_admin import AdminIndexView
from flask_admin import expose,form
from functools import wraps
from ..middleware import has_role
from flask_security import current_user
from flask_admin.contrib.sqla import ModelView
from .utils import MultipleImageUploadField
from . import app
from PIL import Image
import ast

class MyAdminIndexView(AdminIndexView):
    # def is_accessible(self):
    #     return current_user.has_role('admin')
    @expose('/')
    def index(self):
        return super(MyAdminIndexView, self).index()

class UserAdmin(ModelView):
    # def is_accessible(self):
    #     return current_user.has_role('admin')

    column_exclude_list = list = ('password',)

    def _list_thumbnail(view, context, model, name):
        if not model.avatar:
            return None

        def gen_img(filename):
            return '<img src="{}">'.format(url_for('static',
                                                   filename="images/avatars/" + form.thumbgen_filename(model.avatar)))

        return Markup("<br />".join(gen_img(model.avatar) for image in ast.literal_eval(model.avatar)))

    column_formatters = {'avatar': _list_thumbnail}

    form_extra_fields = {'avatar': MultipleImageUploadField("avatar",
                                                            base_path="project/static/images/avatars",
                                                            url_relative_path="images/avatars/",
                                                            thumbnail_size=(64, 64, 1))}

class RoleAdmin(ModelView):
    def is_accessible(self):
        return True
        # return current_user.has_role('admin')

class ItemAdmin(ModelView):
    def is_accessible(self):
        return current_user.has_role('admin')

    def _list_thumbnail(view, context, model, name):
        if not model.images:
            return None

        def gen_img(filename):
            return '<img src="{}">'.format(url_for('static',
                                                   filename="images/products/" + form.thumbgen_filename(model.images)))

        return Markup("<br />".join(gen_img(model.images) for image in ast.literal_eval(model.images)))

    column_formatters = {'images': _list_thumbnail}

    form_extra_fields = {'images': MultipleImageUploadField("Images",
                                                            base_path="project/static/images/products",
                                                            url_relative_path="images/products/",
                                                            thumbnail_size=(64, 64, 1))}

class AdvertisementAdmin(ModelView):
    def is_accessible(self):
        return current_user.has_role('admin')

    def _list_thumbnail(view, context, model, name):
        if not model.images:
            return None

        def gen_img(filename):
            return '<img src="{}">'.format(url_for('static',
                                                   filename="images/ads/" + form.thumbgen_filename(model.images)))

        return Markup("<br />".join(gen_img(model.images) for image in ast.literal_eval(model.images)))

    column_formatters = {'images': _list_thumbnail}

    form_extra_fields = {'images': MultipleImageUploadField("Images",
                                                            base_path="project/static/images/ads",
                                                            url_relative_path="images/ads/",
                                                            thumbnail_size=(64, 64, 1))}

class CategoryAdmin(ModelView):
    def is_accessible(self):
        return current_user.has_role('admin')

    def _list_thumbnail(view, context, model, name):
        if not model.icon:
            return None

        def gen_img(filename):
            return '<img src="{}">'.format(url_for('static',
                                                   filename="images/category/" + form.thumbgen_filename(model.icon)))

        return Markup("<br />".join(gen_img(model.icon) for image in ast.literal_eval(model.icon)))

    column_formatters = {'icon': _list_thumbnail}

    form_extra_fields = {'icon': MultipleImageUploadField("icon",
                                                            base_path="project/static/images/icons/category",
                                                            url_relative_path="images/icons/category/",
                                                            thumbnail_size=(64, 64, 1))}

class ProductAdmin(ModelView):
    def is_accessible(self):
        return current_user.has_role('admin')

class AuctionAdmin(ModelView):
    def is_accessible(self):
        return current_user.has_role('admin')

class AddressAdmin(ModelView):
    def is_accessible(self):
        return current_user.has_role('admin')

class StateAdmin(ModelView):
    def is_accessible(self):
        return current_user.has_role('admin')

class GiftAdmin(ModelView):
    def is_accessible(self):
        return current_user.has_role('admin')

class InsuranceAdmin(ModelView):
    def is_accessible(self):
        return current_user.has_role('admin')

class GarantyAdmin(ModelView):
    def is_accessible(self):
        return current_user.has_role('admin')

class InventoryAdmin(ModelView):
    def is_accessible(self):
        return current_user.has_role('admin')

class ManufactureAdmin(ModelView):
    def is_accessible(self):
        return current_user.has_role('admin')

class OfferAdmin(ModelView):
    def is_accessible(self):
        return current_user.has_role('admin')

class EventAdmin(ModelView):
    def is_accessible(self):
        return current_user.has_role('admin')

class PaymentMethodAdmin(ModelView):
    def is_accessible(self):
        return current_user.has_role('admin')

class ShipmentMethodAdmin(ModelView):
    def is_accessible(self):
        return current_user.has_role('admin')

class OrderAdmin(ModelView):
    def is_accessible(self):
        return current_user.has_role('admin')

class PaymentAdmin(ModelView):
    def is_accessible(self):
        return current_user.has_role('admin')

class ShipmentAdmin(ModelView):
    def is_accessible(self):
        return current_user.has_role('admin')

class PlanAdmin(ModelView):
    def is_accessible(self):
        return current_user.has_role('admin')

class UserPlanAdmin(ModelView):
    def is_accessible(self):
        return current_user.has_role('admin')

class AuctionPlanAdmin(ModelView):
    def is_accessible(self):
        return current_user.has_role('admin')

class UserAuctionParticipationAdmin(ModelView):
    def is_accessible(self):
        return current_user.has_role('admin')

class UserMessageAdmin(ModelView):
    def is_accessible(self):
        return current_user.has_role('admin')

class GuestMessageAdmin(ModelView):
    def is_accessible(self):
        return current_user.has_role('admin')

class PaymentMessageAdmin(ModelView):
    def is_accessible(self):
        return current_user.has_role('admin')
