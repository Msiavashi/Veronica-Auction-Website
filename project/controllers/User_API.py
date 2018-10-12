# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from flask_restful import Resource, reqparse
import os
from os import listdir
from os.path import isfile, join
from ..model import *
from flask import url_for, redirect, render_template, request, abort, make_response , jsonify , session, flash
import json
from project import app
from flask_login import LoginManager, UserMixin,login_required, login_user, logout_user ,current_user
from ..model.user_message import UserMessage
from ..model.user_gift import *
from ..model.order import *
import definitions
from werkzeug.utils import secure_filename
from ..utils import Payload
from definitions import AVATAR_DIR
from definitions import MESSAGE_SUBJECTS
from definitions import MAXIMUM_ORDERS
from definitions import COUPONCODE
import copy
import random
from datetime import datetime
from flask_jwt_extended import JWTManager,jwt_required,jwt_refresh_token_required
from sqlalchemy import or_ , and_

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

parse_payment_account = reqparse.RequestParser()
parse_payment_account.add_argument('first_name', help = 'ورود نام ضروری است', required = True)
parse_payment_account.add_argument('last_name', help = 'ورود نام خانوادگی ضروری است', required = True)
parse_payment_account.add_argument('state', help = 'ورود استان ضروری است', required = True)
parse_payment_account.add_argument('city', help = 'ورود شهر ضروری است', required = True)
parse_payment_account.add_argument('address', help = 'ورود آدرس ضروری است', required = True)
parse_payment_account.add_argument('mobile', help = 'ورود شماره همراه ضروری است', required = True)
parse_payment_account.add_argument('accept_tick', required = False)
parse_payment_account.add_argument('work_place', required = False)
parse_payment_account.add_argument('postal_code', required = False)
parse_payment_account.add_argument('more_info', required = False)
parse_payment_account.add_argument('email', required = False)
parse_payment_account.add_argument('shipment_method',help='ورود روش ارسال الزامی است', required = True)
parse_payment_account.add_argument('payment_method',help='ورود روش پرداخت الزامی است', required = True)



class PaymentsInfo(Resource):
    @jwt_required
    def get(self,pagenum,pagesize):
        payments = Payment.query.filter_by(user_id=current_user.id).order_by('created_at DESC').paginate(pagenum, pagesize, True).items
        paymentSchema = PaymentSchema(many=True)
        return make_response(jsonify(paymentSchema.dump(payments)),200)

class UserBasicInfo(Resource):
    @jwt_required
    def get(self):
        user = User.query.get(current_user.id)
        userSchema = UserSchema()
        return make_response(jsonify(userSchema.dump(user)),200)

    @jwt_required
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
            state = State.query.get(address_data['state'])
            address.state = state
            address.postal_code = address_data['postal_code']
            try:
                db.session.add(address)
                db.session.commit()
                current_user.address = address
            except Exception as e:
                return make_response(jsonify({"message": e.message}), 500)
        else:
            current_user.address.city = address_data['city']
            current_user.address.address = address_data['address']
            state = State.query.get(address_data['state'])
            current_user.address.state = state
            current_user.address.postal_code = address_data['postal_code']

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

        #handle invitor copun code
        invitor_code = request.form.get('invitor-code',None)

        if(invitor_code):

            invitor = User.query.filter_by(username=invitor_code).first()

            if(not invitor):
                msg ="کد معرف مورد نظر موجود نمی باشد"
                return make_response(jsonify({"message":{"error":msg}}),500)
            if(invitor.id == current_user.id):
                msg ="شما قادر به معرفی خود نیستید"
                return make_response(jsonify({"message":{"error":msg}}),500)

            already_invited = current_user.gifts.filter_by(title=COUPONCODE).first()

            if(already_invited):
                msg = "جایزه کد معرفی شما قبلا استفاده شده است"
                return make_response(jsonify({"message":{"error":msg}}),400)

            gift = Gift.query.filter_by(title=COUPONCODE).first()
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

class UserInformation(Resource):
    @jwt_required
    def get(self):

        credit = current_user.credit
        enrolled_auctions = UserAuctionParticipation.query.filter_by(user_id=current_user.id).count()
        invitations = User.query.filter_by(invitor=current_user.username).count()

        bought_items = Order.query.filter_by(user_id = current_user.id, status=OrderStatus.PAID).count()

        won_offers = Offer.query.filter_by(win=True).join(UserPlan).filter_by(user_id = current_user.id).all()

        won_auctions = [auction for offer in won_offers for auction in Auction.query.filter_by(id=offer.auction_id)]

        # won_items_in_auction = [Item.query.filter_by(id=auction.item_id) for auction in won_auctions]

        total_discount = 0
        for auction in won_auctions:
            item = Item.query.filter_by(id = auction.item_id).first()
            offer = Offer.query.filter_by(auction_id = auction.id, win=True).first()
            total_discount += item.price - offer.total_price
        states = State.query.order_by('title').distinct().all()
        state_schema = StateSchema(many=True)

        avatars = []
        for root, dirs, files in os.walk(AVATAR_DIR):
            for filename in files:
                avatars.append({"name":filename})

        info = {
            "total_discount": str(total_discount),
            "won_auctions": len(won_offers),
            "total_boughts": bought_items,
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

    @jwt_required
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
            state = State.query.get(address_data['state'])
            address.state = state
            address.postal_code = address_data['postal_code']
            try:
                db.session.add(address)
                db.session.commit()
                current_user.address = address
            except Exception as e:
                return make_response(jsonify({"message": e.message}), 500)
        else:
            current_user.address.city = address_data['city']
            current_user.address.address = address_data['address']
            state = State.query.get(address_data['state'])
            current_user.address.state = state
            current_user.address.postal_code = address_data['postal_code']

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

        #handle invitor copun code
        invitor_code = request.form.get('invitor-code',None)

        if(invitor_code):

            invitor = User.query.filter_by(username=invitor_code).first()

            if(not invitor):
                msg ="کد معرف مورد نظر موجود نمی باشد"
                return make_response(jsonify({"message":{"error":msg}}),500)
            if(invitor.id == current_user.id):
                msg ="شما قادر به معرفی خود نیستید"
                return make_response(jsonify({"message":{"error":msg}}),500)

            gift = Gift.query.filter_by(title=COUPONCODE).first()
            if gift:
                user_gift = db.session.query(user_gifts).filter_by(user_id=current_user.id, gift_id=gift.id,used=True).first()
                if(user_gift):
                    msg = "جایزه کد معرفی شما قبلا استفاده شده است"
                    return make_response(jsonify({"message":{"error":msg}}),400)
                else:
                    current_user.gifts.append(gift)
                    current_user.credit += gift.amount
                    current_user.invitor = invitor.username
                    invitor.credit += gift.amount
                    db.session.add(invitor)
                    db.session.add(current_user)
                    db.session.commit()
                    # update extra field for relationship
                    stmt = user_gifts.update().where(and_(user_gifts.c.user_id==current_user.id,user_gifts.c.gift_id==gift.id)).values(used=True)
                    db.engine.execute(stmt)


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

    @jwt_required
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
        # flash("پیام با موفقیت ارسال شد")
        # return redirect(url_for('profile'))

parser = reqparse.RequestParser()
parser.add_argument('item_id')

class UserCartOrder(Resource):
    def get(self):

        if current_user.is_authenticated:
            orders = Order.query.filter_by(user_id=current_user.id,status=OrderStatus.UNPAID).order_by('created_at DESC')
            result = []
            order_schema = OrderSchema()
            for order in orders:
                result.append(order_schema.dump(order))

            return make_response(jsonify(result), 200)
        else:
            if "orders" in session:
                return make_response(jsonify(session['orders']), 200)
            else:
                return make_response(jsonify({"msg": "no orders"}), 200)

    def post(self):
        order_schema = OrderSchema(many=True)
        data = request.get_json(force=True)
        item_id = int(data.get("item_id", None))
        total = int(data.get("total", None))
        item = Item.query.get(item_id)

        if current_user.is_authenticated:
            last_order = Order.query.filter_by(user_id=current_user.id,item_id=item_id,status=OrderStatus.UNPAID).first()
            if(last_order):
                msg = "این محصول رو قبلا به سبد خرید اضافه کرده اید"
                return make_response(jsonify({"reason":msg}),400)

            #calculate price base on auction participation
            item_price = (item.price - item.discount) * total
            discount_status = OrderDiscountStatus.REGULAR
            discount = item.discount * total

            auction = current_user.auctions.join(Item).filter_by(id = item.id).first()
            if auction:
                offer = Offer.query.join(Auction).filter_by(id=auction.id).order_by("offers.created_at DESC").first()
                discount_status = OrderDiscountStatus.INAUCTION
                if offer and offer.win:
                    item_price = offer.total_price
                    discount_status = OrderDiscountStatus.AUCTIONWINNER
                    total = 1
                    discount = item.price - offer.total_price
                else:
                    userplan = current_user.user_plans.join(Auction).filter_by(id=auction.id).first()
                    auctionplan = AuctionPlan.query.filter_by(auction_id=auction.id).join(UserPlan).filter_by(id=userplan.id).first()
                    item_price = item.price - auctionplan.discount
                    total = 1
                    discount = auctionplan.discount

            new_order = Order()
            new_order.user = current_user
            new_order.item = item
            new_order.total_cost = item_price
            new_order.discount_status = discount_status
            new_order.status = OrderStatus.UNPAID
            new_order.total = total
            new_order.total_discount = discount
            db.session.add(new_order)
            db.session.commit()

            orders = Order.query.filter_by(user_id=current_user.id).filter(or_(Order.status==OrderStatus.UNPAID,Order.status==OrderStatus.PAYING)).order_by('created_at DESC')
            result = []
            order_schema = OrderSchema()
            for order in orders:
                result.append(order_schema.dump(order))
            return make_response(jsonify(result), 200)
        else:

            if not "orders" in session:
                session['orders'] = []

            founded = False
            order_schema = OrderSchema(many=True)
            founded = next((x for x in session['orders'] if x[0]['item']['id'] == item.id and (x[0]['status'] == OrderStatus.UNPAID or x[0]['status'] == OrderStatus.PAYING)), None)
            if (founded):
                msg = "این محصول رو قبلا به سبد خرید اضافه کرده اید"
                return make_response(jsonify({"reason":msg}),400)

            if len(session['orders']) < MAXIMUM_ORDERS :
                new_order = Order()
                new_order.id = random.randint(1,1000)
                new_order.item = item;
                new_order.total_cost = (item.price - item.discount) * total
                new_order.total = total
                new_order.status = OrderStatus.UNPAID
                new_order.discount_status = OrderDiscountStatus.REGULAR
                new_order.total_discount = item.discount * total
                order_schema = OrderSchema()
                session['orders'].append(order_schema.dump(new_order))
                return make_response(jsonify(session['orders']), 200)
            else:
                return make_response(jsonify({"reason": "حداکثر تعداد سبد خرید شما پر شده است"}), 400)

    def patch(self):
        data = request.get_json(force=True)
        order_id = int(data.get("order_id", None))
        total = int(data.get("total", None))

        if current_user.is_authenticated:
            new_order = Order.query.get(order_id)
            item = new_order.item
            #calculate price base on auction participation
            item_price = (item.price - item.discount) * total
            discount_status = OrderDiscountStatus.REGULAR
            discount = item.discount * total

            auction = current_user.auctions.join(Item).filter_by(id = item.id).first()
            if auction:
                offer = Offer.query.join(Auction).filter_by(id=auction.id).order_by("offers.created_at DESC").first()
                discount_status = OrderDiscountStatus.INAUCTION
                if offer and offer.win:
                    item_price = offer.total_price
                    discount_status = OrderDiscountStatus.AUCTIONWINNER
                    total = 1
                    discount = item.price - offer.total_price
                else:
                    userplan = current_user.user_plans.join(Auction).filter_by(id=auction.id).first()
                    auctionplan = AuctionPlan.query.filter_by(auction_id=auction.id).join(UserPlan).filter_by(id=userplan.id).first()
                    item_price = item.price - auctionplan.discount
                    total = 1
                    discount = auctionplan.discount

            new_order.total_cost = item_price
            new_order.status = OrderStatus.UNPAID
            new_order.discount_status = discount_status
            new_order.total = total
            new_order.total_discount = discount
            db.session.add(new_order)
            db.session.commit()
            orders = Order.query.filter_by(user_id=current_user.id).filter(or_(Order.status==OrderStatus.UNPAID,Order.status==OrderStatus.PAYING)).order_by('created_at DESC')
            # orders = Order.query.filter_by(user_id=current_user.id,status=OrderStatus.UNPAID).order_by('created_at DESC')
            result = []
            order_schema = OrderSchema()
            for order in orders:
                result.append(order_schema.dump(order))
            return make_response(jsonify(result), 200)
        else:
            order = next((x for x in session['orders'] if x[0]['id'] == order_id),None)
            print order[0]
            # print session['orders']

            if ((order[0]['status'] == str(OrderStatus.UNPAID) or order[0]['status'] == str(OrderStatus.PAYING))):
                order[0]['total_cost'] = (order[0]['item']['price'] - order[0]['item']['discount']) * total
                order[0]['total'] = total
                order[0]['total_discount'] = order[0]['item']['discount'] * total

                return make_response(jsonify(session['orders']), 200)

    def delete(self):
        data = request.get_json(force=True)
        order_id = int(data.get("order_id", None))
        order_schema = OrderSchema(many=True)

        if current_user.is_authenticated:
            Order.query.filter_by(id=order_id).delete()
            db.session.commit()

            if len(current_user.orders) == 0:
                for gift in current_user.gifts:
                    user_gift = db.session.query(user_gifts).filter_by(user_id=current_user.id, gift_id=gift.id).first()
                    if not user_gift.used:
                        current_user.gifts.remove(gift)

            db.session.commit()
            orders = Order.query.filter_by(user_id=current_user.id)
            result = []
            order_schema = OrderSchema()
            for order in orders:
                result.append(order_schema.dump(order))

            return make_response(jsonify(result), 200)
        else:
            order = None
            for x in session['orders']:
                if x[0]['id'] == order_id:
                    order = x
                    break
            # order = next(x for x in session['orders'] if x[0]['id'] == order_id)
            if order:
                session['orders'].remove(order)
            return make_response(jsonify(session['orders']), 200)

class UserCartCheckout(Resource):
    @jwt_required
    def get(self):
        if current_user.is_authenticated:
            orders = Order.query.filter_by(user_id=current_user.id,status=OrderStatus.PAYING).order_by('created_at DESC')
            result = []
            order_schema = OrderSchema()
            for order in orders:
                result.append(order_schema.dump(order))

            return make_response(jsonify(result), 200)

class UserCoupons(Resource):
    @jwt_refresh_token_required
    def get(self):
        data = []
        for gift in current_user.gifts:
            user_gift = db.session.query(user_gifts).filter_by(user_id=current_user.id, gift_id=gift.id,used=False).first()
            if user_gift:
                data.append({"code":gift.id,"title":gift.title ,"amount":str(gift.amount)})
            # update extra field for relationship
            # stmt = user_gifts.update().where(user_gifts.c.user_id==current_user.id,user_gifts.c.gift_id==gift.id).values(used=False)
            # db.engine.execute(stmt)

        return make_response(jsonify(data), 200)

    @jwt_required
    def post(self):

        if(not current_user.is_authenticated):
            msg = "کوپن تخفیف فقط برای کاربران عضو تعریف شده است"
            return make_response(jsonify({"reason":msg, "success":False}),400)

        data = request.get_json(force=True)
        coupon_code = data.get("coupon", None)
        #handle invitor copun code
        if(coupon_code):
            coupon = Gift.query.filter_by(title = coupon_code).first()
            if(not coupon):
                msg ="کد تخفیف شما معتبر نمی باشد"
                return make_response(jsonify({"reason":msg}),400)
            if coupon.expired:
                msg =  "کوپن تخفیف مورد نظر منقضی شده است"
                return make_response(jsonify({"reason":msg}),400)

            gift_user = db.session.query(user_gifts).filter_by(user_id=current_user.id, gift_id=coupon.id).first()
            if gift_user:
                if gift_user.used:
                    msg = "کد تخفیف قبلا توسط شما استفاده شده است"
                    return make_response(jsonify({"reason":msg}),400)
                else:
                    msg = "این کوپن تخفیف قبلا برای سبد خرید شما ثبت شده است"
                    return make_response(jsonify({"code":coupon.id, "title":coupon.title, "amount":str(coupon.amount), "reason":msg,"success":True}),200)
            else:
                current_user.gifts.append(coupon)
                db.session.add(current_user)
                db.session.commit()
                msg ="کد تخفیف مورد نظر شما با موفقیت اعمال شد"
                return make_response(jsonify({"code":coupon.id, "title":coupon.title, "amount":str(coupon.amount), "reason":msg,"success":True}),200)

        msg ="لطفا کد تخفیف خود را وارد کنید"
        return make_response(jsonify({"reason":msg}),400)

    @jwt_required
    def delete(self):
        data = request.get_json(force=True)
        coupon_code = data.get("coupon_code", None)
        if coupon_code:
            db_coupon = Gift.query.get(coupon_code)
            user = db_coupon.users.filter_by(id=current_user.id).first()
            db_coupon.users.remove(user)
            db.session.add(db_coupon)
            db.session.commit()
            return make_response(jsonify({"msg":"کوپن خرید شما با موفقیت حذف شد"}), 200)

class UserCheckOutInit(Resource):
    def post(self):
        if (not current_user.is_authenticated):
            if "orders" in session:
                unpaid_orders = session['orders']
                payment = unpaid_orders[0][0]['payment']
                if not payment:
                    payment = Payment()
                else:
                    payment = Payment.query.get(payment[0]['id'])

                payment.type = PaymentType.PRODUCT
                payment.amount = 0
                payment.discount = 0
                payment.status = PaymentStatus.PAYING
                payment.details = str(unpaid_orders[0][0]['id'])

                payment.payment_method = PaymentMethod.query.filter_by(type=Payment_Types.Online).first()
                paymentschema = PaymentSchema()

                for order in unpaid_orders:
                    order[0]['status'] = OrderStatus.PAYING
                    payment.amount += float(order[0]['total_cost'])
                    payment.discount += float(order[0]['total_discount'])

                db.session.add(payment)
                db.session.commit()
                session['orders'][0][0]['payment'] = paymentschema.dump(payment)
        else:
            # unpaid_orders = Order.query.filter_by(user_id=current_user.id, status=OrderStatus.UNPAID).all()

            unpaid_orders = Order.query.filter_by(user_id=current_user.id).filter(or_(Order.status==OrderStatus.UNPAID,Order.status==OrderStatus.PAYING)).all()
            payment = Order.query.filter_by(user_id=current_user.id).filter(or_(Order.status==OrderStatus.UNPAID,Order.status==OrderStatus.PAYING)).first().payment
            if(not payment):
                payment = Payment()

            payment.type = PaymentType.PRODUCT
            payment.amount = 0
            payment.discount = 0

            payment.payment_method = PaymentMethod.query.filter_by(type=Payment_Types.Online).first()
            payment.status = PaymentStatus.PAYING

            gift_discount = 0
            user_gift = db.session.query(user_gifts).filter_by(user_id=current_user.id,used=False).all()
            for g in user_gift:
                gift = Gift.query.get(g.gift_id)
                if not gift.expired:
                    gift_discount += gift.amount
                    # stmt = user_gifts.update().where(and_(user_gifts.c.user_id==current_user.id,user_gifts.c.gift_id==gift.id)).values(used=True)
                    # db.engine.execute(stmt)
                else:
                    stmt = user_gifts.delete().where(and_(user_gifts.c.user_id==current_user.id,user_gifts.c.gift_id==gift.id))
                    db.engine.execute(stmt)

            for order in unpaid_orders:
                payment.amount += order.total_cost
                payment.discount += order.total_discount
                order.status = OrderStatus.PAYING

                if (not order.payment):
                    db.session.add(payment)
                    current_user.payments.append(payment)
                    db.session.add(current_user)

                order.payment = payment
                order.payment_id = payment.id

                db.session.add(order)
            payment.amount -= gift_discount
            payment.discount += gift_discount
            db.session.add(payment)
            db.session.commit()

        msg = "نمایش پیش فاکتور برای سفارش شما"
        return make_response(jsonify({'success':True,"type":"redirect_to_invoice","pid":payment.id,"message":msg}),200)

#TODO: *strict validation*
class UserCheckoutConfirm(Resource):
    def post(self, pid):
        data = parse_payment_account.parse_args()
        shipment_method = data['shipment_method']
        payment_method = data['payment_method']
        payment = Payment.query.get(pid)
        shipment_method = ShipmentMethod.query.get(shipment_method)
        payment_method = PaymentMethod.query.get(payment_method)

        if current_user.is_authenticated:
            print data,data['accept_tick'] == "True"

            if ('accept_tick' in data and data['accept_tick'] == "True"):
                current_user.first_name = data['first_name']
                current_user.last_name = data['last_name']
                current_user.mobile = data['mobile']

                if 'work_place' in data:
                    current_user.work_place = data['work_place']
                if 'email' in data:
                    current_user.email = data['email']

                if(not current_user.address):
                    address = Address()
                    address.city = data['city']
                    address.address = data['address']
                    state = State.query.get(data['state'])
                    address.state = state
                    address.postal_code = data['postal_code']
                    try:
                        db.session.add(address)
                        db.session.commit()
                        current_user.address = address
                    except Exception as e:
                        return make_response(jsonify({"message":{"message": e.message}}), 500)
                else:
                    current_user.address.city = data['city']
                    current_user.address.address = data['address']
                    state = State.query.get(data['state'])
                    current_user.address.state = state
                    current_user.address.postal_code = data['postal_code']

                db.session.add(current_user)
                db.session.commit()

            if not payment:
                msg = "پرداخت معتبری برای سبد خرید شما موجود نیست.لطفا سبد خود را دوباره تشکیل دهید"
                return make_response(jsonify({"message":{"message":msg,"success":False}}),400)

            if payment.user_id != current_user.id:
                msg = "این عملیات پرداخت غیر مجاز است"
                return make_response(jsonify({"message":{"message":msg,"success":False}}),400)

            if payment.status == PaymentStatus.PAID:
                msg = "این صورتحساب قبلا پرداخت شده است"
                return make_response(jsonify({"message":{"message":msg,"operation":"redirect_to_profile","success":False}}),400)

            if payment_method.type == Payment_Types.Credit:
                if current_user.credit < payment.amount + shipment_method.price:
                    msg = "موجودی حساب شما برای پرداخت این صورتحساب کافی نیست"
                    return make_response(jsonify({"message" : {"message":msg,"operation":"redirect_to_profile","success":False}}),400)
                else:
                    current_user.credit -= payment.amount + shipment_method.price
                    db.session.add(current_user)
                    db.session.commit()

                    orders = Order.query.filter_by(payment_id=pid,user_id=current_user.id).all()

                    for order in orders:
                        shipment = Shipment.query.filter_by(order_id=order.id).first()
                        if shipment :
                            shipment.shipment_method = shipment_method
                            shipment.shipment_method_id = shipment_method.id
                            shipment.status = ShipmentStatus.READY_TO_SEND
                        else:
                            shipment = Shipment()
                            shipment.order_id = order.id
                            shipment.payment_id = pid
                            shipment.status = ShipmentStatus.READY_TO_SEND
                            shipment.shipment_method = shipment_method
                            shipment.shipment_method_id = shipment_method.id
                            order.shipment = shipment
                            if ('more_info' in data):
                                order.description = data['more_info']
                            db.session.add(shipment)
                        order.status = OrderStatus.PAID
                        db.session.add(order)

                    payment.amount += shipment_method.price
                    payment.status = PaymentStatus.PAID
                    payment.ref_id = random.randint(100000,10000000)
                    payment.sale_order_id = random.randint(1000000,1000000000)
                    payment.sale_refrence_id = random.randint(1000,1000000)
                    payment.GUID = random.randint(1000000000,100000000000)
                    payment.payment_method = payment_method
                    payment.payment_method_id = payment_method.id

                    user_gift = db.session.query(user_gifts).filter_by(user_id=current_user.id,used=False).all()
                    for g in user_gift:
                        gift = Gift.query.get(g.gift_id)
                        if gift:
                            stmt = user_gifts.update().where(and_(user_gifts.c.user_id==current_user.id,user_gifts.c.gift_id==gift.id)).values(used=True)
                            db.engine.execute(stmt)

                    db.session.add(payment)
                    db.session.commit()
                    msg = "مبلغ مورد نظر از حساب شما کسر شد و خرید با موفقیت انجام گرفت"
                    return make_response(jsonify({"message":{'success':True,"message":msg,"operation":"redirect_to_profile"}}),200)

            if payment_method.type == Payment_Types.Online:

                orders = Order.query.filter_by(payment_id=pid,user_id=current_user.id).all()

                for order in orders:
                    shipment = Shipment.query.filter_by(order_id=order.id).first()
                    if shipment :
                        shipment.shipment_method = shipment_method
                        shipment.shipment_method_id = shipment_method.id
                        shipment.status = ShipmentStatus.IN_STORE
                    else:
                        shipment = Shipment()
                        shipment.order_id = order.id
                        shipment.payment_id = pid
                        shipment.status = ShipmentStatus.IN_STORE
                        shipment.shipment_method = shipment_method
                        shipment.shipment_method_id = shipment_method.id
                        order.shipment = shipment
                        db.session.add(shipment)
                    order.status = OrderStatus.PAYING
                    db.session.add(order)

                payment.amount += shipment_method.price
                payment.payment_method = payment_method
                payment.payment_method_id = payment_method.id
                payment.sale_order_id = random.randint(1000000,1000000000)
                payment.sale_refrence_id = random.randint(1000,1000000)
                payment.GUID = random.randint(1000000000,100000000000)

                db.session.add(payment)
                db.session.commit()

                msg = "هدایت به صفحه تایید نهایی مبلغ و انتخاب درگاه پرداخت"
                return make_response(jsonify({'message':{'success':True,"operation":"redirect_to_bank","pid":payment.id,"message":msg}}),200)
            else:
                msg = "روش پرداخت مورد نظر وجود ندارد"
                return make_response(jsonify({"message":{"message":{"message":msg,"success":False}}}),400)
        else:
            msg = "برای پرداخت صورتحساب باید به سایت وارد شوید"
            return make_response(jsonify({"message":{"message":msg,"success":False}}),400)

class UserApplyPayment(Resource):
    @jwt_required
    def get(self,pid):
        payment = Payment.query.get(pid)

        unpaid_user_plan = UserPlan.query.filter_by(payment_id=payment.id, user_id = current_user.id).first()

        if(payment.status == PaymentStatus.PAID):

            orders = Order.query.filter_by(payment_id=pid).all()

            if(unpaid_user_plan):
                if(not current_user.has_auction(unpaid_user_plan.auction)):
                    current_user.auctions.append(unpaid_user_plan.auction)
            elif(orders):
                for order in orders:
                    shipment = Shipment.query.filter_by(order_id=order.id).first()
                    shipment.status = ShipmentStatus.READY_TO_SEND
                    order.status = OrderStatus.PAID

                    user_gift = db.session.query(user_gifts).filter_by(user_id=current_user.id,used=False).all()
                    for g in user_gift:
                        gift = Gift.query.get(g.gift_id)
                        if gift:
                            stmt = user_gifts.update().where(and_(user_gifts.c.user_id==current_user.id,user_gifts.c.gift_id==gift.id)).values(used=True)
                            db.engine.execute(stmt)

                    db.session.add(shipment)
            else:
                current_user.credit += payment.amount
                db.session.add(current_user)
            db.session.commit()
            msg = "پرداخت موفق"
            return make_response(jsonify({"success":True,"message":msg,"token":payment.ref_id}),200)
        else:
            if unpaid_user_plan:
                UserPlan.query.filter_by(payment_id=payment.id, user_id = current_user.id).delete()
                db.session.commit()

            msg = "پرداخت ناموفق"
            return make_response(jsonify({"success":False,"message":msg,"token":payment.ref_id}),200)

class UserUnpaidOrders(Resource):
    @jwt_required
    def get(self):
        unpaid_orders = Order.query.filter_by(status=OrderStatus.UNPAID, user_id = current_user.id).all()
        order_schema = OrderSchema(many=True)
        return make_response(jsonify(order_schema.dump(unpaid_orders)), 200)

class UserUnpaidPayments(Resource):
    @jwt_required
    def get(self):
        unpaid_payments = Payment.query.filter_by(user_id=current_user.id, status=PaymentStatus.UNPAID).all()
        payment_schema = PaymentSchema(many=True)
        return make_response(jsonify(payment_schema.dump(unpaid_payments)), 200)

class UserAuctionLikes(Resource):
    def get(self):
        if(current_user.is_authenticated):
            return make_response(jsonify(AuctionSchema(many=True).dump(current_user.auction_likes)),200)
        else:
            return make_response(jsonify({"success":False,"message":"برای مشاهده علاقمندی ها باید لاگین کنید"}),400)

    def post(self):
        if current_user.is_authenticated:
            data = request.get_json(force=True)
            auction_id = data['auction_id']
            auction = Auction.query.get(auction_id)
            if(not auction in current_user.auction_likes):
                auction.likes.append(current_user)
                db.session.add(auction)
                db.session.commit()
                return make_response(jsonify({"success":"true","message":"حراجی به علاقمندی های شما اضافه شد"}),200)
            else:
                auction.likes.remove(current_user)
                db.session.add(auction)
                db.session.commit()
                return make_response(jsonify({"success":"true","message":"حراجی از علاقمندی های شما حذف شد"}),200)

        else:
            return make_response(jsonify({"message":"برای لایک کردن باید به سایت وارد شوید"}),400)

    #TODO: create new Route for this
    def delete(self):
        if current_user.is_authenticated:
            data = request.get_json(force=True)
            auction_id = data['auction_id']
            auction = Auction.query.get(auction_id)
            auction.likes.remove(current_user)
            db.session.add(auction)
            db.session.commit()
            return make_response(jsonify({"success":"true","message":"حراجی از علاقمندی های شما حذف شد"}),200)
        else:
            return make_response(jsonify({"message":"برای حذف لایک باید به سایت وارد شوید"}),400)

class UserFavoriteFilters(Resource):
    def get(self,order_by_price,order_by,total):
        now = datetime.now()
        result = None
        if order_by_price == "price":
            result = current_user.auction_likes.join(Item).order_by("price "+order_by).limit(total)
        else:
            result = current_user.auction_likes.order_by("start_date "+order_by).limit(total)

        auctions=[]
        for a in result:
            auction = Auction.query.get(a.id)
            auction.remained_time = (auction.start_date - now).days * 24 * 60 * 60 + (auction.start_date - now).seconds
            auction.left_from_created = (auction.created_at - now).seconds
            auctions.append(auction)

        auction_schema = AuctionSchema(many=True)
        return make_response(jsonify(auction_schema.dump(auctions)),200)

class UserAuctionView(Resource):

    def get(self):
        if current_user.is_authenticated:
            auction_views = db.session.query(user_auction_views).filter_by(user_id = current_user.id).all()
            auctions = [Auction.query.get(auction_view.id) for auction_view in auction_views]
            auction_schema = AuctionSchema(many=True)
            print auctions
            return make_response(jsonify({"seen_auctions": auction_schema.dump(auctions)}), 200)
        else:
            return make_response(jsonify([]), 200)

    @jwt_required
    def post(self):
        data = request.get_json(force=True)
        auction_id = data.get('aid')
        auction = Auction.query.get(auction_id)
        if not db.session.query(user_auction_views).filter_by(user_id=current_user.id, auction_id=auction_id).scalar():
            current_user.auction_views.append(auction)
            db.session.add(current_user)
            db.session.commit()
            return make_response(jsonify({"success": True, "message": {"success": "حراجی به لیست مشاهده شده افزوده شد"}}), 200)
        return make_response(jsonify({"success": False, "message": {"failure": "این جراجی قبلا به لیست مشاهده شده افزوده شده است"}}), 406)


class UserChargeWalet(Resource):
    @jwt_required
    def post(self):
        data = request.get_json(force=True)
        charge_amount = data.get("charge_amount", None)

        payment_method = PaymentMethod.query.filter_by(type = Payment_Types.Online).first()

        payment = Payment()

        payment.type = PaymentType.WALET
        payment.amount = charge_amount
        payment.payment_method = payment_method
        payment.status = PaymentStatus.UNPAID
        payment.discount = 0

        current_user.payments.append(payment)
        db.session.add(current_user)
        db.session.commit()

        msg = " برای پرداخت به صفحه تایید هدایت می شوید"
        return make_response(jsonify({'success':True,"type":"redirect_to_bank","pid":payment.id,"message":msg}),200)
