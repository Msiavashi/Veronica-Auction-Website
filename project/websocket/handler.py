from project.database import db
from project.model import *

from flask import url_for, redirect, render_template, request, abort, make_response , jsonify , session
import json
from project import app
from datetime import datetime
from flask_login import LoginManager, UserMixin,login_required, login_user, logout_user ,current_user

def offer_bid(data):
    try:
        auction = Auction.query.get(data['auction_id'])
        user = User.query.get(data['user_id'])
        plan = Plan.query.join(auction_plans).filter_by(auction_id=auction.id).first()

        offer = Offer()
        offer.user_id = user.id
        offer.item_id = auction.item.id
        # if(plan.total_offers > 0):
        #     plan.total_offers = plan.total_offers - 1
        #     db.session.add(plan)
        main_plan = Plan.query.get(plan.id)
        offer.offer_price = (main_plan.price // main_plan.total_offers ) * auction.rate
        #
        db.session.add(offer)
        db.session.commit()

        offers = db.session.query(db.func.count(offers.id).label('total')).join(Auction)
        # result = db.session.query(Auction.id, db.func.count(user_auction_likes.c.user_id).label('total')).join(user_auction_likes).group_by(Auction.id).having(Auction.end_date >= today).order_by('total DESC')

        return "{'success':'true','auction':"+auction.name+",'user':"+user.username+"'offers:'"+offers+"}"
    except Exception as e:
        return "{'error':"+str(e)+"}"
