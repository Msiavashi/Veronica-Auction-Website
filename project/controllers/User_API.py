# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from flask_restful import Resource, reqparse
import os
from ..model import *
from flask import url_for, redirect, render_template, request, abort, make_response , jsonify , session, flash, session
import json
from project import app
from datetime import datetime
from flask_login import LoginManager, UserMixin,login_required, login_user, logout_user ,current_user
from ..model.user_message import UserMessage
import definitions
from werkzeug.utils import secure_filename
from ..model import Order
from ..model import Item




class PaymentsInfo(Resource):
    @login_required
    def get(self):
        current_user = User.query.filter_by(username="mohammad").first()
        pagenum = int(request.args.get('pagenum'))
        pagesize = int(request.args.get('pagesize'))

        payments = Payment.query.filter_by(user_id=current_user.id).paginate(pagenum, pagesize, True).items
        paymentSchema = PaymentSchema(many=True)
        return make_response(jsonify(paymentSchema.dump(payments)),200)


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

        info = {
            "credit": str(credit),
            "total_discount": str(total_discount),
            "won_auctions": len(won_auctions),
            "total_orders": len(bought_items),
            "total_enrolled_auctions": enrolled_auctions,
            "total_invitations": invitations,
            "invitation_code": current_user.username
        }
        print info
        return make_response(jsonify(info),200)

    @login_required
    def post(self):
        # json_data = request.get_json(force=True)
        print request.form
        current_user.alias_name = request.form.get('alias-name')
        current_user.first_name = request.form.get('first-name')
        current_user.last_name = request.form.get('last-name')
        current_user.work_place = request.form.get('work-place')
        current_user.mobile = request.form.get('mobile')
        current_user.email = request.form.get('email')

        address = Address()
        address.city = request.form.get('city', None)
        address.address = request.form.get('address', None)
        address.state = request.form.get('state', None)
        address.postal_code = request.form.get('postal-code', None)
        address.country = "iran"

        try:
            db.session.add(address)
            db.session.commit()
        except Exception as e:
            return jsonify({"msg": "could not save changes"}), 500

        current_user.address = address
        current_user.invitor = request.form.get('invitor-code')
        current_user.avatar_index = request.form.get('avatar-index')

        old_password = request.form.get('current-password')
        new_password = request.form.get('new-password')
        repeat_password = request.form.get('confirm-password')
        if not User.verify_hash(old_password, current_user.password):
            return jsonify({"msg": "پسوورد اشتباه است"}), 403
        
        if new_password != repeat_password:
            return jsonify({"msg": "رمز جدید با تکرار رمز همخوانی ندارد"}), 403
        
        current_user.password = User.generate_hash(new_password)

        #verifying invitor code
        if User.query.filter_by(invitor=current_user.invitor).exists():
            return jsonify({"msg": "کد دعوت قبلا استفاده شده است"}), 400

        #TODO: check this with MohammadReza
        elif User.query.filter_by(username=current_user.invitor).exists():
            #TODO: check the gift values and create a table to store these kind of values
            current_user.credit += 10000
            invitor = User.query.filter_by(username=current_user.invitor).first()
            invitor.credit += 20000
            db.session.add(invitor)
            db.session.commit()
        else:
            return jsonify({"msg": "کد دعوت وارد شده صحیح نمیباشد"}), 400

        try:
            db.session.add(current_user)
            db.session.commit()
            flash("تغییرات با موفقیت ذخیره شد")
            return redirect(url_for('profile'))
        except Exception as e:
            return jsonify({"msg": "could not save changes"}), 500


        

class UserContactUs(Resource):

    def _allowed_file(self, filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in definitions.ALLOWED_EXTENTIONS

    @login_required
    def post(self): 
        new_message = UserMessage()

        new_message.title = request.form.get('title', None)
        new_message.subject = request.form.get('subject', None)
        new_message.message = request.form.get('message', None)

        if 'file' in request.files:
            file = request.files['file']
            if file and self._allowed_file(file.filename):
                filename = secure_filename(file.filename)
                path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(path)
                new_message.file = path

        db.session.add(new_message)
        db.session.commit()
        flash("پیام با موفقیت ارسال شد")
        return redirect(url_for('profile'))

class CartOrder(Resource):
    def get(self):
        if current_user.is_authenticated:
            orders = Order.query.all()
            order_schema = OrderSchema()
            return make_response(jsonify(order_schema.dump(orders), 200))

        else:
            order = Order()
            order.items = [Item.query.get(item_id) for item_id in session['items']]
            order.total_cost += sum([item.price for item in order.items])
            order_schema = OrderSchema()
            return make_response(jsonify(order_schema.dump(order)), 200)

    def post(self, data):
        data = data.get_json(force=True)
        if current_user.is_authenticated:
            last_order = Order.query.order_by('created_at DESC').limit(1).first()
            item = Item.query.filter_by(id=data['item_id']).first()
            if last_order.status == 0: #if unpaid
                last_order.append(item)
                last_order.total_cost += item.price
                db.session.add(last_order)
                db.session.commit()
                return make_response(jsonify({"msg": "آیتم انتخاب شده به سبد خرید اضافه شد", "items": [item.id for item in last_order.items]}), 200)

            else:
                new_order = Order()
                new_order.user_id = current_user.id
                new_order.items.append(item)
                new_order.total_cost += item.price
                new_order.register_user = True
                db.session.add(new_order)
                db.session.commit()
                return make_response( jsonify({"msg": "آیتم انتخاب شده به سبد خرید اضافه شد", "items": [item.id]}), 200)

        else:
            if not "items" in session:
                session['items'] = list()
            session['items'].append(data['item_id'])
            return make_response(jsonify({"msg": "آیتم انتخاب شده به سبد خرید اضافه شد", "items": session['items']}), 200)




                

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
