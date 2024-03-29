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
from ..model import *
from sqlalchemy import or_ , and_
from sqlalchemy import func
from project.database import db

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
        user_auction_participants = User.query.join(UserAuctionParticipation).count()
        avg_auction_users = ("%.2f" % (float(user_auction_participants)/float(auctions)))
        online_payments = db.session.query(func.sum(Payment.amount).label('total')).filter_by(status=100,payment_method_id=1).scalar()
        wallet_charge = db.session.query(func.sum(Payment.amount).label('total')).filter_by(status=100,type='2000',payment_method_id=1).scalar()
        buy_plan = db.session.query(func.sum(Payment.amount).label('total')).filter_by(status=100,type='1000',payment_method_id=1).scalar()
        buy_product = db.session.query(func.sum(Payment.amount).label('total')).filter_by(status=100,type='3000',payment_method_id=1).scalar()
        free_payments = Payment.query.filter_by(status=100,type='4000').count()
        total_shipment_walet = db.session.query((func.sum(ShipmentMethod.price).label('total'))).join(Shipment).join(Order).join(Payment).filter(Payment.status==100,Payment.type=='3000',Payment.payment_method_id==2).scalar()
        total_shipment_online = db.session.query((func.sum(ShipmentMethod.price).label('total'))).join(Shipment).join(Order).join(Payment).filter(Payment.status==100,Payment.type=='3000',Payment.payment_method_id==1).scalar()
        paid_shipment = Shipment.query.join(Order).join(Payment).filter(Payment.status==100,Payment.type=='3000').count()
        online_payment_discounts = db.session.query(func.sum(Payment.discount).label('total')).filter_by(status=100,payment_method_id=1).scalar()
        all_wins = 0
        items_total_price = 0
        offers = Offer.query.filter_by(win=True).all()
        for offer in offers:
            all_wins += offer.total_price
            items_total_price += offer.auction.item.price


        self._template_args['auctions'] = auctions
        self._template_args['users'] = users
        self._template_args['payments'] = payments
        self._template_args['orders'] = orders
        self._template_args['user_auction_participants'] = user_auction_participants
        self._template_args['avg_auction_users'] = avg_auction_users
        self._template_args['online_payments'] = int(online_payments)
        self._template_args['wallet_charge'] = int(wallet_charge)
        self._template_args['buy_plan'] = int(buy_plan)
        self._template_args['free_payments'] = free_payments
        self._template_args['paid_shipment'] = paid_shipment
        self._template_args['online_payment_discounts'] = int(online_payment_discounts)
        self._template_args['potantial_discounts'] = int(items_total_price - all_wins)

        if buy_product:
            self._template_args['buy_product'] = int(buy_product)
        else:
            self._template_args['buy_product'] = 0

        if total_shipment_walet:
            self._template_args['total_shipment_walet'] = int(total_shipment_walet)
        else:
            self._template_args['total_shipment_walet'] = 0

        if total_shipment_online:
            self._template_args['total_shipment_online'] = int(total_shipment_online)
        else:
            self._template_args['total_shipment_online'] = 0


        return super(MyAdminIndexView, self).index()

class UserAdmin(ModelView):
    page_size = 10
    can_view_details = True
    column_searchable_list = ['first_name', 'last_name','alias_name','username','mobile','address.city','address.state.title','address.address','address.postal_code','is_verified']
    column_editable_list = ['first_name', 'last_name','alias_name','credit','is_active','is_banned','is_verified','mobile','send_sms_attempts','login_attempts','verification_attempts']
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
    page_size = 10
    can_view_details = True
    column_searchable_list = ['title', 'description','show']
    column_editable_list = ['title', 'description','show','link','link_title','discount']
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
    column_editable_list = ['win']
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
    column_editable_list = ['status', 'discount_status','total']

    def is_accessible(self):
        return current_user.has_role('admin')

class PaymentAdmin(ModelView):
    page_size = 10
    can_view_details = True
    column_searchable_list = ['user.first_name','user.last_name','user.alias_name','user.username','payment_method.title','GUID', 'ref_id','status','amount','type']
    column_editable_list = ['status','type']
    column_exclude_list = ['sale_order_id','sale_refrence_id','details']

    def is_accessible(self):
        # return True
        return current_user.has_role('admin')

class ShipmentAdmin(ModelView):
    page_size = 10
    can_view_details = True
    column_editable_list = ['status','send_date','recieve_date']
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
    page_size = 10
    can_view_details = True
    column_searchable_list = ['title','subject','message','user.username','user.first_name','user.last_name','user.alias_name']
    def is_accessible(self):
        return current_user.has_role('admin')

class GuestMessageAdmin(ModelView):
    def is_accessible(self):
        return current_user.has_role('admin')

class PaymentMessageAdmin(ModelView):
    def is_accessible(self):
        return current_user.has_role('admin')

class NotificationAdmin(ModelView):
    def is_accessible(self):
        return current_user.has_role('admin')

class UserNotificationAdmin(ModelView):
    page_size = 10
    can_view_details = True
    column_searchable_list = ['notification.text','notification.title','user.username','user.mobile']
    column_editable_list = ['delivered','seen','send_sms']
    def is_accessible(self):
        return current_user.has_role('admin')

class AuctionNotificationAdmin(ModelView):
    def is_accessible(self):
        return current_user.has_role('admin')

class UserAuctionNotificationAdmin(ModelView):
    def is_accessible(self):
        return current_user.has_role('admin')

class SMSAdmin(ModelView):
    page_size = 10
    can_view_details = True
    column_searchable_list = ['delivered', 'status_code','text','title','user.username','user.mobile']
    column_editable_list = ['delivered']
    def is_accessible(self):
        return current_user.has_role('admin')
