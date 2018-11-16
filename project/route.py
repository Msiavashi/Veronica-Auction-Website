# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from flask import url_for, redirect, render_template, request, abort ,redirect, session,jsonify
from datetime import timedelta
from flask_login import current_user,login_required,logout_user
from .model import *
from . import app,login_manager,verify_required,iverify_required
from urlparse import urlparse, urljoin
from .controllers.Payment_API import MellatGateway
from definitions import *
import time
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    jwt_refresh_token_required, create_refresh_token,
    get_jwt_identity, set_access_cookies,
    set_refresh_cookies, unset_jwt_cookies
)
from sqlalchemy import or_
# from .model.payment import *


class Route():

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    # @app.route('/documentation')
    # def documentation():
    #     return auto.html()

    @app.route('/')
    def site():
        return render_template('site/index.html')

    @app.route('/login/')
    def account_login():
        if current_user.is_authenticated:
            return redirect('/')

        next = request.args.get('next')

        if next and ( "participate" in next or "instantview" in next):
            return render_template('site/iframes/ilogin.html', next=next)
        return render_template('site/login.html',next=next)

    @app.route('/verify')
    def account_verify():
        if current_user.is_authenticated:
            return redirect('/')
        if not "username" in session:
            return redirect('/login')
        next = request.args.get('next')
        return render_template('site/verify.html',next=next)

    @app.route('/forgotpassword')
    def account_forgot():
        if current_user.is_authenticated:
            return redirect('/')

        next = request.args.get('next')
        return render_template('site/forgot.html',next=next)

    @app.route('/iforgot')
    def account_iforgot():
        if current_user.is_authenticated:
            return redirect('/')

        next = request.args.get('next')
        return render_template('site/iframes/iforgot.html',next=next)





    @app.route('/ilogin')
    def ilogin():
        if current_user.is_authenticated:
            return redirect('/')
        next = request.args.get('next')
        return render_template('site/iframes/ilogin.html',next=next)

    @app.route('/iverify')
    def iverify():
        if current_user.is_authenticated:
            return redirect('/')
        next = request.args.get('next')
        return render_template('site/iframes/iverify.html',next=next)

    @app.route('/register/')
    def account_register():
        if current_user.is_authenticated:
            return redirect('/')
        next = request.args.get('next')
        if next:
            return render_template('site/register.html',next=next)

        return render_template('site/register.html')


    @app.route('/iregister')
    def iregister():
        if current_user.is_authenticated:
            return redirect('/')
        return render_template('site/iframes/iregister.html')

    @app.route("/logout")
    @login_required
    def logout():
        resp = jsonify({'logout': True})
        unset_jwt_cookies(resp)
        logout_user()
        return redirect('/')

    @app.route("/profile")
    @login_required
    @verify_required
    def profile():
        return render_template('site/profile.html',tab='default')

    @app.route("/profile/<tab>")
    @login_required
    @verify_required
    def profile_tab(tab):
        print "tab",tab
        if tab == "":
            return render_template('site/profile.html',tab='default')

        tabs = {'modify','sendmessage','payments','invitor','walet','changepass'}
        if tab in tabs:
            return render_template('site/profile.html',tab=tab)
        return abort(404)

    @app.route("/favorite")
    @login_required
    def favorite():
        return render_template('site/favorite.html')

    @app.route("/search")
    def search():
        keyword = request.args.get('keyword')
        return render_template('site/search.html',keyword=keyword)

    @app.route("/participate/<int:aid>")
    @login_required
    @iverify_required
    def participate(aid):
        if(not current_user.has_auction(aid)):
            return render_template('site/iframes/package.html',auction_id=aid)
        return redirect(url_for('viewAuction',aid=aid))

    @app.route("/instantview/<int:aid>")
    @login_required
    def instantview(aid):
        if(current_user and not current_user.has_auction(aid)):
            return render_template('site/iframes/package.html',auction_id=aid)
        return render_template('site/iframes/quickview.html',auction_id=aid)
        # if(current_user.is_authenticated and not current_user.has_auction(aid)):
        # return render_template('site/iframes/quickview-guest.html',auction_id=aid)

    @app.route("/view/auction/<int:aid>")
    @login_required
    def viewAuction(aid):
        auction = Auction.query.get(aid)
        if auction:
            return render_template('site/auction.html',auction_id=aid)
        else:
            abort(404)

    @app.route("/view/category/<int:cid>/products")
    def viewProducts(cid):
        return render_template('site/products.html',category_id=cid)

    @app.route("/view/auctions")
    def viewAuctions():
        return render_template('site/held.html')

    @login_manager.unauthorized_handler
    def unauthorized():
        # next = url_for(request.endpoint,**request.view_args)
        print request.endpoint
        if reuquest.endpoint == "participate" or request.endpoint == "instantview":
            next += "iframe";
        return render_template('site/401.html',next=next), 401

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('site/404.html'), 404

    @app.errorhandler(403)
    def page_not_found(e):
        return render_template('site/403.html'), 403


    @app.route('/about')
    def about():
        return render_template('site/about.html')

    # @app.route('/user/<int:id>')
    # @auto.doc()
    # def show_user(id):
    #     return id

    @app.route('/confirm/payment/<int:pid>')
    @login_required
    def confirm(pid):
        payment = Payment.query.get(pid)
        if(payment.status != PaymentStatus.PAID):
            amount = payment.amount
            return render_template('site/iframes/confirm.html',amount=amount,pid=pid)
        return render_template('site/404.html'), 404

    @app.route('/callback/payment/<int:pid>')
    def callback(pid):
        return render_template('site/iframes/callback.html',pid=pid)

    @app.route('/faq')
    def faq():
        return render_template('site/faq.html')

    @app.route('/roles')
    def roles():
        return render_template('site/roles.html')

    @app.route('/iroles')
    def iroles():
        return render_template('site/iframes/iroles.html')

    @app.route('/help')
    def help():
        return render_template('site/help.html')

    @app.route('/howworks')
    def howworks():
        return render_template('site/howworks.html')

    @app.route('/private')
    def private():
        return render_template('site/private.html')

    @app.route('/contact')
    def contact():
        return render_template('site/contact.html')

    @app.route('/news')
    def news():
        return render_template('site/news.html')

    @app.route('/socket')
    def socket():
        return render_template('/socket.html')

    @app.route('/checkout/payment/<int:pid>')
    # @login_required
    def checkout_payment(pid):
        order_payment = None
        if current_user.is_authenticated:
            unpaid_orders = Order.query.filter_by(user_id=current_user.id).filter(or_(Order.status==OrderStatus.UNPAID,Order.status==OrderStatus.PAYING)).first()
            if unpaid_orders:
                order_payment = unpaid_orders.payment
        else:
            order = session['orders'][0]
            payment_id = int(order[0]['payment'][0]['id'])
            order_payment = Payment.query.get(payment_id)
        current_payment = Payment.query.get(pid)

        if current_payment and order_payment and current_payment.id == order_payment.id:
            return render_template('site/checkout.html', pid=pid)
        else:
            abort(404)

    @app.route('/checkout')
    @login_required
    def checkout():
        unpaid_payment = Payment.query.filter_by(user_id=current_user.id, status=PaymentStatus.UNPAID).first()
        return redirect(url_for('checkout_payment', pid=unpaid_payment.id))

    @app.route('/cart')
    @verify_required
    def cart():
        return render_template('site/cart.html')


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

route = Route()
