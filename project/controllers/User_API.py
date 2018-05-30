# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from flask_restful import Resource, reqparse
import os
from os import listdir
from os.path import isfile, join
from ..model import *
from flask import url_for, redirect, render_template, request, abort, make_response , jsonify , session, flash, session
import json
from project import app
from datetime import datetime
from flask_login import LoginManager, UserMixin,login_required, login_user, logout_user ,current_user
from ..model.user_message import UserMessage
from ..model.order import OrderStatus
import definitions
from werkzeug.utils import secure_filename
from ..utils import PythonObjectEncoder
from definitions import AVATAR_DIR
from definitions import MESSAGE_SUBJECTS


class PaymentsInfo(Resource):
    @login_required
    def get(self,pagenum,pagesize):
        payments = Payment.query.filter_by(user_id=current_user.id).paginate(pagenum, pagesize, True).items
        paymentSchema = PaymentSchema(many=True)
        return make_response(jsonify(paymentSchema.dump(payments)),200)

parser_user_address = reqparse.RequestParser()
parser_user_address.add_argument('state', help = 'ورود استان ضروری است', required = True)
parser_user_address.add_argument('city', help = 'ورود شهر ضروری است', required = True)
parser_user_address.add_argument('address', help = 'ورود آدرس ضروری است', required = True)
parser_user_address.add_argument('postal_code', help = 'ورود کد پستی ضروری است', required = True)

parser_user_account = reqparse.RequestParser()
parser_user_account.add_argument('mobile', help = 'ورود شماره تلفن ضروری است', required = True)

parser_user_message = reqparse.RequestParser()
parser_user_message.add_argument('subject', help = 'ورود موضوع پیام ضروری است', required = True)
parser_user_message.add_argument('title', help = 'ورود عنوان پیام ضروری است', required = True)
parser_user_message.add_argument('message', help = 'متنی برای پیام وارد نکرده اید', required = True)


class UserInformation(Resource):
    @login_required
    def get(self):

        credit = current_user.credit
        enrolled_auctions = UserAuctionParticipation.query.filter_by(user_id=current_user.id).count()
        invitations = User.query.filter_by(invitor=current_user.username).count()

        bought_items = [item for order in Order.query.filter_by(user_id = current_user.id, status=1).all() for item in order.items]

        won_offers = Offer.query.filter_by(win=True).join(UserPlan).filter_by(user_id = current_user.id).all()

        won_auctions = [auction for offer in won_offers for auction in Auction.query.filter_by(id=offer.auction_id)]

        # won_items_in_auction = [Item.query.filter_by(id=auction.item_id) for auction in won_auctions]

        total_discount = 0
        for auction in won_auctions:
            item = Item.query.filter_by(id = auction.item_id).first()
            offer = Offer.query.filter_by(auction_id = auction.id, win=True).first()
            total_discount += item.price - offer.total_price
        states = State.query.order_by('title DESC').distinct().all()
        state_schema = StateSchema(many=True)

        avatars = []
        for root, dirs, files in os.walk(AVATAR_DIR):
            for filename in files:
                avatars.append({"name":filename})

        info = {
            "credit": str(credit),
            "total_discount": str(total_discount),
            "won_auctions": len(won_auctions),
            "total_boughts": len(bought_items),
            "total_enrolled_auctions": enrolled_auctions,
            "total_invitations": invitations,
            "invitation_code": current_user.username,
            "states":state_schema.dump(states),
            "info":UserSchema().dump(current_user),
            "avatars":avatars,
            "subjects":MESSAGE_SUBJECTS
        }
        print info
        return make_response(jsonify(info),200)

    @login_required
    def post(self):
        # json_data = request.get_json(force=True)

        user_data = parser_user_account.parse_args()

        current_user.alias_name = request.form.get('alias-name')
        current_user.first_name = request.form.get('first-name')
        current_user.last_name = request.form.get('last-name')
        current_user.work_place = request.form.get('work-place')
        current_user.mobile = user_data['mobile']
        current_user.email = request.form.get('email')

        address_data = parser_user_address.parse_args()

        if(not current_user.address):
            address = Address()
            address.city = address_data['city']
            address.address = address_data['address']
            address.state = State.query.get(address_data['state'])
            address.postal_code = address_data['postal_code']
            address.country = "iran"
            current_user.address = address
            try:
                db.session.add(address)
                db.session.commit()
            except Exception as e:
                return make_response(jsonify({"message": e.message}), 500)
        else:
            current_user.address.city = address_data['city']
            current_user.address.address = address_data['address']
            current_user.address.state = State.query.get(address_data['state'])
            current_user.address.postal_code = address_data['postal_code']
            current_user.address.country = "iran"

        avatar_index = request.form.get('avatar-index',None)
        if(avatar_index):
            current_user.avatar = "['"+request.form.get('avatar-index')+"']"

        old_password = request.form.get('current-password',None)
        new_password = request.form.get('password',None)
        repeat_password = request.form.get('c_password',None)

        if new_password :
            if not User.verify_hash(old_password, current_user.password):
                msg = " رمز عبور قبلی شما نادرست است"
                return  make_response(jsonify({"message":{"error":msg}}),403)

            if new_password != repeat_password:
                msg = "رمز عبور جدید با تکرار رمز عبور همخوانی ندارد"
                return make_response(jsonify({"message": {"confirm-password":msg}}),403)

            current_user.password = User.generate_hash(new_password)

        invitor_code = request.form.get('invitor-code',None)

        if(invitor_code):
            print invitor_code

            invitor = User.query.filter_by(username=invitor_code).first()

            if(not invitor):
                msg ="کد معرف مورد نظر موجود نمی باشد"
                return make_response(jsonify({"message":{"error":msg}}),500)
            if(invitor.id == current_user.id):
                msg ="شما قادر به معرفی خود نیستید"
                return make_response(jsonify({"message":{"error":msg}}),500)

            already_invited = current_user.gifts.filter_by(title='invitor').first()
            if(already_invited):
                msg = "جایزه کد معرفی شما قبلا استفاده شده است"
                return make_response(jsonify({"message":{"error":msg}}),400)

            gift = Gift.query.filter_by(title='invitor').first()
            current_user.gifts.append(gift)
            current_user.credit += gift.amount
            current_user.invitor = invitor.username
            invitor.credit += gift.amount
            db.session.add(invitor)
            db.session.commit()

        try:
            db.session.add(current_user)
            db.session.commit()
            msg = " اطلاعات شما با موفقیت ذخیره شد "
            if new_password :
                logout_user()
            return make_response(jsonify({"message":{"success":msg}}),200)
        except Exception as e:
            return make_response(jsonify({"message":{"error":e.message}}), 500)

class UserContactUs(Resource):

    def _allowed_file(self, filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in definitions.ALLOWED_EXTENTIONS

    @login_required
    def post(self):
        user_message = parser_user_message.parse_args()

        new_message = UserMessage()
        new_message.title = user_message['title']
        new_message.subject = user_message['subject']
        new_message.message = user_message['message']
        new_message.user = current_user
        print request
        if 'file' in request.files:
            file = request.files['file']
            if file and self._allowed_file(file.filename):
                filename = secure_filename(file.filename)
                print filename
                path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(path)
                new_message.file = path
            else:
                msg ="نوع فایل انتخابی شما مناسب نمی باشد"
                return make_response(jsonify({"message":{"success":{"error":msg}}}),500)

        db.session.add(new_message)
        db.session.commit()
        msg ="پیام شما با موفقیت ارسال شد. در اولین فرصت جهت پیگیری با شما تماس خواهیم گرفت"
        return make_response(jsonify({"message":{"success":msg}}),200)

class CartOrder(Resource):

    def get(self):
        if current_user.is_authenticated:
            orders = Order.query.filter_by(status=OrderStatus.UNPAID, user_id=current_user.id).all()
            order_schema = OrderSchema()
            return make_response(jsonify(order_schema.dump(orders), 200))

        else:
            orders = session['orders']
            order_schema = OrderSchema()
            return make_response(jsonify(order_schema.dump(orders)), 200)

    def post(self, data):
        order_schema = OrderSchema()
        data = data.get_json(force=True)
        if current_user.is_authenticated:
            item = Item.query.filter_by(id=data['item_id']).first()
            quantity = data['quantity']
            if quantity > item.quantity:
                return make_response(jsonify({"message": {"error": "تعداد درخواست شده موجود نیست"}}), 400)

            new_order = Order()
            new_order.item_id = item.id
            new_order.total = quantity
            new_order.total_cost = ( quantity * item.price ) - item.discount
            new_order.user = current_user.id

            db.session.add(new_order)
            db.session.commit()
            return make_response(jsonify({"message": {"success": "به سبک خرید اضافه شد"}, "unpaid_orders": jsonify(order_schema.dump( Order.query.filter_by(user_id=current_user.id, status=OrderStatus.UNPAID ).all() ))}), 200)

        else:
            if not "orders" in session:
                session['orders'] = list()
            new_order = Order()
            new_order.item_id = item.id
            new_order.total = quantity
            new_order.total_cost = ( quantity * item.price ) - item.discount
            new_order.user = current_user.id
            session['orders'].append(new_order)
            return make_response(jsonify({"message": {"success": "به سبک خرید اضافه شد"}, "unpaid_orders": jsonify(OrderSchema.dump(session['orders']))}), 200)




                

#TODO: *strict validation*
class Checkout(Resource):

    @login_required
    def post(self):
        data = request.get_json(force=True)
        order_id = data['order_id']
        order = Order.query.get(order_id)
        if not order or not order.user_id == current_user.id:
            return make_response(jsonify({"msg": "سبد خرید مورد نظر یافت نشد"}) , 400)

        payment = Payment()
        payment.amount = order.total_cost
        payment.order_id = order_id
        payment.user_id = current_user.id

        payment_method = PaymentMethod()
        payment_method.title = data['payment_method']       #TODO: validation with enum

        db.session.add(payment_method)
        db.session.add.commit()

        payment.payment_method_id = payment_method.id

        db.session.add(payment)
        db.session.commit()

        shipment = Shipment()
        shipment.order_id = order.id
        shipment.payment_id = payment.id


        shipment_method = ShipmentMethod()
        shipment_method.title = data['shipment_method']
        shipment_method.price = data['shipmet_price']

        db.session.add(shipment_method)
        db.session.commit()

        shipment.shipment_method_id = shipment_method.id

        db.session.add(shipment)
        db.session.commit()

        order.total_cost += shipment_method.price
        order.payment_id = payment.id

        db.session.add(order)
        db.session.commit()

        return make_response(jsonify({'success': True}, 200))
