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
from ..model.user_gift import *
from ..model.order import OrderStatus
import definitions
from werkzeug.utils import secure_filename
from ..utils import Payload
from definitions import AVATAR_DIR
from definitions import MESSAGE_SUBJECTS
from definitions import MAXIMUM_ORDERS
import copy


class PaymentsInfo(Resource):
    @login_required
    def get(self,pagenum,pagesize):
        payments = Payment.query.filter_by(user_id=current_user.id).order_by('created_at DESC').paginate(pagenum, pagesize, True).items
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
        # flash("پیام با موفقیت ارسال شد")
        # return redirect(url_for('profile'))

parser = reqparse.RequestParser()
parser.add_argument('item_id')



class UserCartOrder(Resource):
    def get(self):

        if current_user.is_authenticated:
            orders = Order.query.filter_by(user_id=current_user.id)
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
        item_id = request.get_json('item_id')['item_id']
        total = request.get_json('total')['total']
        item = Item.query.get(item_id)

        if current_user.is_authenticated:
            last_order = Order.query.filter_by(user_id=current_user.id,item_id=item_id).first()
            if(last_order):
                msg = " این محصول در سبد خرید شما از قبل موجود است"
                return make_response(jsonify({"reason":msg}),400)
            new_order = Order()
            new_order.user = current_user
            new_order.item = item
            new_order.total_cost = item.price - item.discount
            new_order.status = 0
            new_order.total = total
            new_order.total_discount = item.discount

            db.session.add(new_order)
            db.session.commit()
            orders = Order.query.filter_by(user_id=current_user.id).all()
            return make_response(jsonify(order_schema.dump(orders)), 200)
        else:

            if not "orders" in session:
                session['orders'] = []

            founded = False
            order_schema = OrderSchema(many=True)
            for order in session['orders']:
                p = order_schema.load(order)
                if (int(p.data[0]['item']['id']) == item.id):
                    founded = True
                    break

            if (founded):
                msg = " این محصول در سبد خرید شما از قبل موجود است"
                return make_response(jsonify({"reason":msg}),400)


            if len(session['orders']) < MAXIMUM_ORDERS :
                new_order = Order()
                new_order.id = 1000
                new_order.item = item;
                new_order.total_cost = item.price
                new_order.total = total
                new_order.status = 0
                new_order.total_discount = item.discount
                order_schema = OrderSchema()
                session['orders'].append(order_schema.dump(new_order))
                return make_response(jsonify(session['orders']), 200)
            else:
                return make_response(jsonify({"reason": "حداکثر تعداد سبد خرید شما پر شده است"}), 400)


class UserCouponApply(Resource):

    @login_required
    def post(self):
        data = request.get_json(force=True)
        coupon_id = int(data.get("coupon", None))
        user_gift = db.session.query(user_gifts).filter_by(user_id=current_user.id, gift_id=coupon_id).first()
        if user_gift and user_gift.used==False:
            user_gift.used = True
            db.session.add(user_gift)
            db.session.commit()
            return make_response(jsonify({"success": True}), 200)
        else:
            return make_response(jsonify({"success": False, "message": {"error": "کد تخفیف معتبر نمی باشد"}}), 406)



#TODO: fix this
class UserCartUpdate(Resource):

    def post(self):

        data = request.get_json(force=True)["user_orders"]
        if current_user.is_authenticated:
            for order in data:
                order = order[0]
                db_order = Order.query.get(order["id"])
                db_order.total = order.get("total")
                db_order.total_cost = (int(order['total']) * int((order['item']['price']) - int(order['item']['discount'])))
                db.session.add(db_order)
                db.session.commit()
            return make_response(jsonify({"success": True}), 200)
        else:
            orders = session['orders']
            order = filter(lambda order: order.id == data['order_id'], orders)
            order.total = data['quantity']
            order.total_cost = (order.total * (order.item.price - order.item.discount))

    def delete(self):
        print request

class UserCartOrderDelete(Resource):
    def post(self):
        order_schema = OrderSchema(many=True)
        print request.data
        order_id = request.get_json(force=True)['order_id']
        print order_id

        if current_user.is_authenticated:
            order = Order.query.filter_by(id=order_id).first()
            db.session.delete(order)
            db.session.commit()
            orders = Order.query.filter_by(user_id=current_user.id)
            return make_response(jsonify(order_schema.dump(orders)), 200)
        else:
            order_schema = OrderSchema(many=True)
            new_orders = session['orders'].filter(lambda order: order.id != order_id)
            session['orders']= new_orders
            return make_response(jsonify(session['orders']), 200)

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
            auction.likes.append(current_user)
            db.session.add(auction)
            db.session.commit()
            return make_response(jsonify({"success":"true","message":"حراجی به علاقمندی های شما اضافه شد"}),200)
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


class CheckOutInit(Resource):
    @login_required
    def post(self):
        unpaid_orders = Order.query.filter_by(user_id=current_user.id, status=OrderStatus.UNPAID).all()
        payment = Payment()
        payment.amount = 0

        # TODO: make PaymentMethod nullable in database
        payment_method = PaymentMethod.query.all()[0]
        payment.payment_method = payment_method

        db.session.add(payment)
        db.session.commit()
        current_user.payments.append(payment)
        db.session.add(current_user)
        for order in unpaid_orders:
            payment.amount += order.total_cost
            order.payment = payment
            order.payment_id = payment.id
            db.session.add(order)
            db.session.commit()

        return redirect(url_for('checkout_payment', pid=payment.id))




#TODO: *strict validation*
class UserCheckoutConfirm(Resource):
    @login_required
    def post(self, pid):
        payment_method_id = request.form.get('payment_method_id')
        shipment_method_id = request.form.get('shipment_method_id')
        final_price = request.form.get('final_price')
        payment = Payment.query.get(pid)

        if not payment or payment.user_id != current_user.id:
            return make_response(jsonify({"msg": "سبد خرید مورد نظر یافت نشد"}) , 400)

        shipment_method = ShipmentMethod.query.get(shipment_method_id)
        payment_method = PaymentMethod.query.get(payment_method_id)

        payment.payment_method = payment_method
        payment.payment_method_id = payment_method_id

        orders = Order.query.filter_by(payment_id=pid).all()

        for order in orders:
            shipment = Shipment()
            shipment.order_id = order.id
            shipment.payment_id = pid
            shipment.status = ShipmentStatus.IN_STORE
            shipment.shipment_method = shipment_method
            shipment.shipment_method_id = shipment_method_id

            db.session.add(shipment)
            db.session.commit()

            order.shipment = shipment

            db.session.add(order)
            db.session.commit()


        payment.amount = final_price

        db.session.add(payment)
        db.session.commit()

        if payment_method.type == Payment_Types.Online:
            return redirect('/checkout/payment/%s' % pid)
        else:
            return make_response(jsonify({'success': False, "message": {"error": "روش پرداخت مورد نظر وجود ندارد"}}, 406))


class UserApplyPayment(Resource):
    @login_required
    def get(self,pid):
        payment = Payment.query.get(pid)

        unpaid_user_plan = UserPlan.query.filter_by(payment_id=payment.id, user_id = current_user.id).first()
        if(payment.status == PaymentStatus.PAID):

            order = Order.query.filter_by(payment_id=payment.id).first()

            if(order):
                pass
            elif(unpaid_user_plan):
                if(not current_user.has_auction(unpaid_user_plan.auction)):
                    current_user.auctions.append(unpaid_user_plan.auction)
            else:
                current_user.credit += payment.amount

            db.session.add(current_user)
            db.session.commit()
            msg = "پرداخت شما با موفقیت انجام شد"
            return make_response(jsonify({"success":True,"message":msg,"token":payment.ref_id}),200)
        else:
            unpaid_user_plan = UserPlan.query.filter_by(payment_id=payment.id, user_id = current_user.id).delete()
            db.session.commit()
            msg = "پرداخت شما موفقیت آمیز نبود"
            return make_response(jsonify({"success":False,"message":msg,"token":payment.ref_id}),400)

class UserUnpaidOrders(Resource):

    @login_required
    def get(self):
        unpaid_orders = Order.query.filter_by(status=OrderStatus.UNPAID, user_id = current_user.id).all()
        order_schema = OrderSchema(many=True)
        return make_response(jsonify(order_schema.dump(unpaid_orders)), 200)


class UserUnpaidPayments(Resource):

    @login_required
    def get(self):
        unpaid_payments = Payment.query.filter_by(user_id=current_user.id, status=PaymentStatus.UNPAID).all()
        payment_schema = PaymentSchema(many=True)
        return make_response(jsonify(payment_schema.dump(unpaid_payments)), 200)

class UserAuctionView(Resource):

    # def get(self):
        # if current_user.is_authenticated:
        #     auction_views = db.session.query(user_auction_views).filter_by(user_id = current_user.id).all()
        #     auctions = [Auction.query.get(auction_view.id) for auction_view in auction_views]
        #     auction_schema = AuctionSchema(many=True)
        #     print auctions
        #     return make_response(jsonify({"seen_auctions": auction_schema.dump(auctions)}), 200)
        # else:
        #     return make_response(jsonify([]), 200)



    def post(self):
        if current_user.is_authenticated:
            data = request.get_json(force=True)
            auction_id = data.get('aid')
            auction = Auction.query.get(auction_id)
            if not db.session.query(user_auction_views).filter_by(user_id=current_user.id, auction_id=auction_id).scalar():
                current_user.auction_views.append(auction)
                db.session.add(current_user)
                db.session.commit()
                return make_response(jsonify({"success": True, "message": {"success": "حراجی به لیست مشاهده شده افزوده شد"}}), 200)
            return make_response(jsonify({"success": False, "message": {"failure": "این جراجی قبلا به لیست مشاهده شده افزوده شده است"}}), 406)
        else:
            pass
