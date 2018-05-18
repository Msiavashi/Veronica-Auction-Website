# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import gevent
from flask import url_for, redirect, render_template, request, abort ,redirect, session
from datetime import timedelta
from flask import render_template, jsonify
from flask_login import current_user,login_required,logout_user,LoginManager
from .model import *
from . import app
from definitions import SESSION_EXPIRE_TIME


class Route():

    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    @app.before_request
    def make_session_permanent():
        session.permanent = True
        permanent_session_lifetime = timedelta(minutes=SESSION_EXPIRE_TIME)
        session.modified = True

    @app.route('/')
    def site():
        return render_template('site/index.html')

    @app.route('/login/')
    def account_login():
        if current_user.is_authenticated:
            return redirect('/')
        return render_template('site/login.html')

    @app.route('/ilogin')
    def ilogin():
        if current_user.is_authenticated:
            return redirect('/')
        return render_template('site/iframes/ilogin.html')

    @app.route('/register/')
    def account_register():
        if current_user.is_authenticated:
            return redirect('/')
        return render_template('site/register.html')

    @app.route('/iregister')
    def iregister():
        if current_user.is_authenticated:
            return redirect('/')
        return render_template('site/iframes/iregister.html')

    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        return redirect('/')

    @app.route("/profile")
    @login_required
    def profile():
        return render_template('site/profile.html')

    @app.route("/participate/<int:aid>")
    # @login_required
    def participate(aid):
        return render_template('site/iframes/package.html',auction_id=aid)

    @app.route("/instantview/<int:aid>")
    @login_required
    def instantview(aid):
        return render_template('site/iframes/quickview.html',auction_id=aid)

    @app.route("/view/auction/<int:aid>")
    # @login_required
    def viewAuction(aid):
        return render_template('site/auction.html',auction_id=aid)


    @login_manager.unauthorized_handler
    def unauthorized():
        return render_template('site/401.html'), 401

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('site/404.html'), 404

    @app.route('/about')
    def about():
        return render_template('site/about.html')

    @app.route('/faq')
    def faq():
        return render_template('site/faq.html')

    @app.route('/contact')
    def contact():
        return render_template('site/contact.html')

    @app.route('/news')
    def news():
        return render_template('site/news.html')

    @app.route('/socket')
    def socket():
        return render_template('/socket.html')

route = Route()
