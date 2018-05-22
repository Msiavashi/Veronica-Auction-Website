# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from flask_restful import Resource, reqparse, abort
import os
from ..model import *
from flask import url_for, redirect, render_template, request, abort, make_response , jsonify , session, flash
import json
from project import app
from datetime import datetime
from flask_login import LoginManager, UserMixin,login_required, login_user, logout_user ,current_user
from ..model.order import PaymentStatus
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



class DashBoard(Resource):
    @login_required
    def get(self):

        credit = current_user.credit
        enrolled_auctions = UserAuctionParticipation.query.filter_by(user_id=current_user.id).count()
        invitations = User.query.filter_by(invitor=current_user.username).count()

        bought_items = [item for order in Order.query.filter_by(user_id = current_user.id, status=PaymentStatus.paid).all() for item in order.items]

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


class UserContactUs(Resource):

    def _allowed_file(self, filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in definitions.ALLOWED_EXTENTIONS

    @login_required
    def post(self): 

        new_message = UserMessage()

        new_message.title = request.get.json('title', None)
        new_message.subject = request.get.json('subject', None)
        new_message.message = request.get.json('message', None)

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
    
    @login_required
    def editInforamtion(self):
        if not request.is_json:
            return jsonify({"success": False, "msg": "no json input"}), 400
        
        # json_data = request.get_json(force=True)
        current_user.alias_name = request.form.get('alias_name')
        current_user.first_name = request.form.get('first_name')
        current_user.last_name = request.form.get('last_name')
        current_user.work_place = request.form.get('work_place')
        current_user.mobile = request.form.get('mobile')
        current_user.email = request.form.get('email')

        address = Address()
        address.city = request.form.get('city')
        address.address = request.form.get('address')
        address.state = request.form.get('state')
        address.postal_code = request.form.get('postal_code')
        address.country = "iran"

        db.session.add(address)
        db.session.commit()

        current_user.address = address
        current_user.invitor = request.form.get('invitor_code')
        current_user.avatar_index = request.form.get('avatar_index')

        old_password = request.form.get('old_password')
        new_password = request.form.get('new_password')
        repeat_password = request.form.get('repeat_password')

        if sha256.hash(old_password) != current_user.password:
            return jsonify({"msg": "پسوورد اشتباه است"}), 403
        
        if new_password != repeat_password:
            return jsonify({"msg": "رمز جدید با تکرار رمز همخوانی ندارد"}), 403
        
        current_user.password = new_password
        db.session.add(current_user)
        db.session.commit()
        


