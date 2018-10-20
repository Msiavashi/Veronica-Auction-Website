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
from ..model import User,Auction,Payment,Order

class MyAdminIndexView(AdminIndexView):

    @expose('/admin/', methods=('GET', 'POST'))
    def edit_view(self):
         users = User.query.count()
         print "users :",users
         return super(AdminIndexView, users=users).edit_view()

    def is_accessible(self):
        # return True
        return current_user.has_role('admin')

    @expose('/')
    def index(self):
        auctions = Auction.query.count()
        users = User.query.count()
        payments = Payment.query.count()
        orders = Order.query.count()
        self._template_args['auctions'] = auctions
        self._template_args['users'] = users
        self._template_args['payments'] = payments
        self._template_args['orders'] = orders
        return super(MyAdminIndexView, self).index()

class UserAdmin(ModelView):
    page_size = 10
    can_view_details = True
    column_searchable_list = ['first_name', 'last_name','alias_name','username']
    column_editable_list = ['first_name', 'last_name','credit']
    column_exclude_list = ['email','updated_at']
    def is_accessible(self):
        # return True
        return current_user.has_role('admin')


    column_exclude_list = list = ('password',)

    def _list_thumbnail(view, context, model, name):
        if not model.avatar:
            return None

        def gen_img(filename):
            return '<img src="{}">'.format(url_for('static',filename="images/avatars/" + form.thumbgen_filename(model.avatar).split("'")[1]))

        return Markup("<br />".join(gen_img(model.avatar) for image in ast.literal_eval(model.avatar)))

    column_formatters = {'avatar': _list_thumbnail}

    form_extra_fields = {'avatar': MultipleImageUploadField("avatar",
                                                            base_path="project/static/images/avatars",
                                                            url_relative_path="images/avatars/",
                                                            thumbnail_size=(64, 64, 1))}

class RoleAdmin(ModelView):
    def is_accessible(self):
        # return True
        return current_user.has_role('admin')

class ItemAdmin(ModelView):
    page_size = 10
    can_view_details = True
    column_searchable_list = ['title', 'description']
    column_editable_list = ['title', 'description','price','quantity','discount']
    column_exclude_list = ['description', ]
    form_widget_args = {
    'description': {
    'rows': 10,
    'style': 'color: black'
    }
    }

    def is_accessible(self):
        return current_user.has_role('admin')

    def _list_thumbnail(view, context, model, name):
        if not model.images:
            return None

        def gen_img(filename):
            return '<img src="{}">'.format(url_for('static',
                                                   filename="images/products/" + form.thumbgen_filename(model.images).split("'")[1]))

        return Markup("<br />".join(gen_img(model.images) for image in ast.literal_eval(model.images)))

    column_formatters = {'images': _list_thumbnail}

    form_extra_fields = {'images': MultipleImageUploadField("Images",
                                                            base_path="project/static/images/products",
                                                            url_relative_path="images/products/",
                                                            thumbnail_size=(64, 64, 1))}

class AdvertisementAdmin(ModelView):
    def is_accessible(self):
        # return True
        return current_user.has_role('admin')

    def _list_thumbnail(view, context, model, name):
        if not model.images:
            return None

        def gen_img(filename):
            return '<img src="{}">'.format(url_for('static',
                                                   filename="images/ads/" + form.thumbgen_filename(model.images).split("'")[1]))

        return Markup("<br />".join(gen_img(model.images) for image in ast.literal_eval(model.images)))

    column_formatters = {'images': _list_thumbnail}

    form_extra_fields = {'images': MultipleImageUploadField("Images",
                                                            base_path="project/static/images/ads",
                                                            url_relative_path="images/ads/",
                                                            thumbnail_size=(64, 128, 1))}

class CategoryAdmin(ModelView):
    def is_accessible(self):
        # return True
        return current_user.has_role('admin')

    def _list_thumbnail(view, context, model, name):
        if not model.icon:
            return None

        def gen_img(filename):
            return '<img src="{}">'.format(url_for('static',
                                                   filename="images/category/" + form.thumbgen_filename(model.icon).split("'")[1]))

        return Markup("<br />".join(gen_img(model.icon) for image in ast.literal_eval(model.icon)))

    column_formatters = {'icon': _list_thumbnail}

    form_extra_fields = {'icon': MultipleImageUploadField("icon",
                                                            base_path="project/static/images/icons/category",
                                                            url_relative_path="images/icons/category/",
                                                            thumbnail_size=(64, 64, 1))}

class ProductAdmin(ModelView):
    page_size = 10
    can_view_details = True
    column_searchable_list = ['title', 'description']
    column_editable_list = ['title', 'description']
    column_exclude_list = ['description', ]
    form_widget_args = {
    'description': {
    'rows': 10,
    'style': 'color: black'
    }
    }

    def is_accessible(self):
        # return True
        return current_user.has_role('admin')

class AuctionAdmin(ModelView):
    page_size = 10
    can_view_details = True
    column_searchable_list = ['title', 'description']
    column_editable_list = ['title', 'description','start_date']
    column_exclude_list = ['description', ]
    form_widget_args = {
    'description': {
    'rows': 10,
    'style': 'color: black'
    }
    }
    def is_accessible(self):
        # return True
        return current_user.has_role('admin')


class AddressAdmin(ModelView):
    def is_accessible(self):
        # return True
        return current_user.has_role('admin')

class StateAdmin(ModelView):
    def is_accessible(self):
        # return True
        return current_user.has_role('admin')

class GiftAdmin(ModelView):
    def is_accessible(self):
        # return True
        return current_user.has_role('admin')

class InsuranceAdmin(ModelView):
    def is_accessible(self):
        # return True
        return current_user.has_role('admin')

class GarantyAdmin(ModelView):
    def is_accessible(self):
        # return True
        return current_user.has_role('admin')

class InventoryAdmin(ModelView):
    def is_accessible(self):
        # return True
        return current_user.has_role('admin')

class ManufactureAdmin(ModelView):
    def is_accessible(self):
        # return True
        return current_user.has_role('admin')

class OfferAdmin(ModelView):
    page_size = 30
    can_view_details = True
    column_searchable_list = ['user_plan.auction_plan.plan.title','user_plan.user.first_name','user_plan.user.last_name','user_plan.user.alias_name','user_plan.user.username','auction.title','win']

    def is_accessible(self):
        # return True
        return current_user.has_role('admin')

class EventAdmin(ModelView):
    def is_accessible(self):
        # return True
        return current_user.has_role('admin')

class PaymentMethodAdmin(ModelView):
    def is_accessible(self):
        # return True
        return current_user.has_role('admin')

class ShipmentMethodAdmin(ModelView):
    def is_accessible(self):
        # return True
        return current_user.has_role('admin')

class OrderAdmin(ModelView):
    page_size = 10
    can_view_details = True
    column_searchable_list = ['status','discount_status','item.title','item.product.title','user.first_name','user.last_name','user.alias_name','user.username','payment.GUID', 'payment.ref_id','payment.status','payment.amount','payment.type']

    def is_accessible(self):
        return current_user.has_role('admin')

class PaymentAdmin(ModelView):
    page_size = 10
    can_view_details = True
    column_searchable_list = ['user.first_name','user.last_name','user.alias_name','user.username','payment_method.title','GUID', 'ref_id','status','amount','type']
    column_exclude_list = ['sale_order_id','sale_refrence_id','details']

    def is_accessible(self):
        # return True
        return current_user.has_role('admin')

class ShipmentAdmin(ModelView):
    page_size = 10
    can_view_details = True
    column_searchable_list = ['guid','status','order.status','order.discount_status','order.item.title','order.item.product.title','order.user.first_name','order.user.last_name','order.user.alias_name','order.user.username','order.payment.GUID', 'order.payment.ref_id','order.payment.status','order.payment.amount','order.payment.type','insurance.company']

    def is_accessible(self):
        # return True
        return current_user.has_role('admin')

class PlanAdmin(ModelView):
    def is_accessible(self):
        return current_user.has_role('admin')

class UserPlanAdmin(ModelView):
    page_size = 10
    can_view_details = True
    column_searchable_list = ['user.first_name','user.last_name','user.alias_name','user.username','auction.title','auction_plan.plan.title','payment.status','payment.GUID']
    def is_accessible(self):
        return current_user.has_role('admin')

class AuctionPlanAdmin(ModelView):
    page_size = 10
    can_view_details = True
    column_searchable_list = ['auction.title','plan.title','price','max_offers','discount']
    def is_accessible(self):
        return current_user.has_role('admin')

class UserAuctionParticipationAdmin(ModelView):
    page_size = 10
    can_view_details = True
    column_searchable_list = ['user.first_name','user.last_name','user.alias_name','user.username','auction.title']
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
