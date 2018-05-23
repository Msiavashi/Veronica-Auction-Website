# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


from flask_restful import Resource, reqparse
import os
from ..model import *
from flask import url_for, redirect, render_template, request, abort, make_response , jsonify , session, flash
import json
from project import app
from datetime import datetime
from flask_login import LoginManager, UserMixin,login_required, login_user, logout_user ,current_user
from ..model.user_message import UserMessage
import definitions
from werkzeug.utils import secure_filename




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
