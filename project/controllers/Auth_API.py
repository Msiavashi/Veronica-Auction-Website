#*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from flask_restful import Resource, reqparse
from project.model.user import *
from flask_jwt_extended import (set_refresh_cookies,create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt,set_access_cookies)
from flask import url_for, redirect, render_template, request, abort, make_response , jsonify , session
from ..model import *
from ..model.order import *
import json
from ..database import db
from project import app
from flask_login import LoginManager, UserMixin,login_required, login_user, logout_user ,current_user
from ..melipayamak import SendSMS
from definitions import MAX_LOGIN_ATTEMPTS, MAX_ACTIVATION_ATTEMPTS, MAX_DEFFER_ACTIVATION_TIME, MAX_MESSAGES_SEND, MAX_AVAILABLE_MESSAGE_TIME,COUPONCODE,MAX_INVITOR_POLICY
from datetime import datetime,timedelta

parser_register = reqparse.RequestParser()
parser_register.add_argument('username', help = 'ورود نام کاربری ضروری است', required = True)
parser_register.add_argument('password', help = 'ورود رمز عبور ضروری است', required = True)
parser_register.add_argument('c_password', help = 'ورود تکرار رمز عبور ضروری است', required = True)
parser_register.add_argument('mobile', help = 'ورود شماره موبایل ضروری است', required = True)
parser_register.add_argument('accept_roles', help = 'تایید مقررات سایت الزامی است', required = True)

parser_login = reqparse.RequestParser()
parser_login.add_argument('username', help = 'ورود نام کاربری ضروری است', required = True)
parser_login.add_argument('password', help = 'ورود رمز عبور ضروری است', required = True)
parser_login.add_argument('remember_me', required = False)
parser_login.add_argument('next')

parser_verify = reqparse.RequestParser()
parser_verify.add_argument('code', help = 'ورود کد فعالسازی الزامی است', required = True)

parser_forgot = reqparse.RequestParser()
parser_forgot.add_argument('mobile', help = 'ورود شماره موبایل ضروری است', required = True)

parser_change = reqparse.RequestParser()
parser_change.add_argument('old_password', help = 'ورود رمزعبور فعلی ضروری است', required = True)
parser_change.add_argument('new_password', help = 'ورود رمز عبور جدید ضروری است', required = True)
parser_change.add_argument('confirm_password', help = 'ورود تکرار رمز عبور جدید ضروری است', required = True)

# def can_access(f):
#     if not hasattr(f, 'access_control'):
#         return True
#     return _eval_access(**f.access_control) == AccessResult.ALLOWED

class UserRegistration(Resource):
    def post(self):
        parser_register.parse_args()
        data = request.get_json(force=True)

        if User.find_by_username(data['username'].lower()):
            return make_response(jsonify({"message":{"success":False,"field":"username","text":'کاربری با این مشخصات از قبل تعریف شده است'}}),400)

        if data['username'].isdigit():
            return make_response(jsonify({"message":{"success":False,"field":"username","text":'نام کاربری شما نمی تواند بصورت عدد باشد'}}),400)

        if len(data['username']) > 32 or len(data['username']) < 3:
            return make_response(jsonify({"message":{"success":False,"field":"username","text":'نام کاربری انتخاب شده باید حداقل ۳حرفی و یا حداکثر ۳۲ حرفی باشد.'}}),400)

        if len(data['password']) > 32 or len(data['password']) < 4:
            return make_response(jsonify({"message":{"success":False,"field":"password","text":'رمز عبور انتخابی شما باید حداقل ۴ وحداکثر ۳۲ کاراکتری باشد'}}),400)

        if(data['password']!=data['c_password']):
            return make_response(jsonify({"message":{"success":False,"field":"c_password","text": 'رمز عبور با تکرار آن مطابقت ندارد'}}),400)

        if User.find_by_mobile(data['mobile']):
            return make_response(jsonify({"message":{"success":False,"field":"mobile","text":'این شماره موبایل از قبل در سیستم موجود است'}}),400)

        if len(data['mobile']) > 13 or len(data['mobile']) < 11 or not data['mobile'].isdigit():
            return make_response(jsonify({"message":{"success":False,"field":"mobile","text":'شماره موبایل وارد شده معتبر نیست'}}),400)

        invitor = data.get("invitor", None)

        if invitor:
            if not User.find_by_username(data['invitor']):
                msg = "کاربری با کد معرفی مورد نظر شما وجود ندارد. لطفا کد معرف خود را بطور صحیح وارد کنید ویا این قسمت را خالی رها کنید. "
                return make_response(jsonify({"message":{"success":False,"field":"invitor","text":msg}}),400)

            if User.query.filter_by(invitor=data['invitor']).count() >= MAX_INVITOR_POLICY:
                msg = ".معرف شما از حداکثر تعداد معرفی شدگان خود استفاده کرده است" \
                +" دقت فرمایید که هرفرد تنها قادر به معرفی "+MAX_INVITOR_POLICY+" نفر است."
                return make_response(jsonify({"message":{"success":False,"field":"invitor","text":msg}}),400)

        try:
            new_user = User(data['username'].lower())
            new_user.username = data['username'].lower()
            new_user.mobile = data['mobile']
            new_user.password = User.generate_hash(data['password'])
            new_user.invitor = invitor

            new_user.save_to_db()
            expires = timedelta(days=365)
            access_token = create_access_token(identity = data['username'].lower(),expires_delta=expires)
            refresh_token = create_refresh_token(identity = data['username'].lower(),expires_delta=expires)

            current_user = User.find_by_username(data['username'].lower())

            session['username'] = current_user.username

            resp = jsonify({
                'message': 'Logged in as {}'.format(current_user.username),
                'access_token': access_token,
                'refresh_token': refresh_token
                })

            # login_user(current_user,remember=False)
            # set_refresh_cookies(resp, refresh_token)
            # set_access_cookies(resp, access_token)

            return make_response(resp,200)
        except Exception as e:
            return make_response(jsonify({"message":{"error" : str(e)}}), 500)
    def get(self):
        return make_response(jsonify({"message":"online resources register"}),404)

class UserLogin(Resource):
    def post(self):
        parser_login.parse_args()
        data = request.get_json(force=True)

        current_user = User.find_by_username(data['username'].lower())

        if not current_user:
            return make_response(jsonify({"message" :{"success":False,"field":"username","text":'کاربری با نام کاربری مورد نظر شما پیدا نشد'}}),400)

        if current_user.login_attempts == MAX_LOGIN_ATTEMPTS:
            current_user.is_verified = False
            current_user.is_banned = True
            current_user.is_active = False
            db.session.add(current_user)
            db.session.commit()
            msg = "حساب  کاربری شما موقتا به حالت تعلیق در آمد لطفا با پشتیبانی سایت تماس حاصل کنید"
            return make_response(jsonify({'message':{"success":False,"field":"banned","text": msg}}),401)

        if User.verify_hash(data['password'], current_user.password):

            if current_user.is_banned:
                msg = "متاسفانه حساب کاربری شما در لیست سیاه قرار گرفته است"
                return make_response(jsonify({'message':{"success":False,"field":"blacklist","text": msg}}),401)

            if not current_user.is_verified:
                session['username'] = current_user.username
                msg = "حساب کاربری شما باید از طریق شماره همراه فعال سازی شود"
                return make_response(jsonify({'message':{"success":False,"field":"verification","text":msg}}),401)

            expires = timedelta(days=31)
            access_token = create_access_token(identity = data['username'].lower(),expires_delta=expires)
            refresh_token = create_refresh_token(identity = data['username'].lower(),expires_delta=expires)

            # Set the JWT cookies in the response
            redirect_to_auction = False
            auction_id = 0

            if 'next' in data and "participate" in data['next'] :
                temp = data['next']
                auction_id = temp.split('/')[2]
                if(current_user.has_auction(int(auction_id))):
                    redirect_to_auction = True

            if redirect_to_auction:
                resp = jsonify({
                    'message': 'Logged in as {}'.format(current_user.username),
                    'access_token': access_token,
                    'refresh_token': refresh_token,
                    'redirect_to_auction': redirect_to_auction,
                    'auction_id':auction_id
                    })
            else:
                resp = jsonify({
                    'message': 'Logged in as {}'.format(current_user.username),
                    'access_token': access_token,
                    'refresh_token': refresh_token
                    })

            # create orders from session on login
            if "orders" in session:
                order_schema = OrderSchema(many=True)
                for order in session['orders']:
                    new_order = Order()
                    item = Item.query.get(order[0]['item']['id'])
                    saved_before = Order.query.filter_by(user_id=current_user.id).join(Item).filter_by(id=item.id).first()
                    if not saved_before:
                        #calculate price base on auction participation
                        total = int(order[0]['total'])
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

                        new_order.item = item
                        new_order.total_cost = item_price
                        new_order.total = total
                        new_order.status = OrderStatus.UNPAID
                        new_order.discount_status = discount_status
                        new_order.total_discount = discount
                        new_order.user = current_user;
                        db.session.add(new_order)
                        db.session.commit()
                session.pop('orders')

            # if 'remember_me' in data and data['remember_me']==True:
            #     login_user(current_user,remember=True)
            # else:
            #     login_user(current_user,remember=False)

            expire_date = timedelta(days=31)
            set_refresh_cookies(resp, refresh_token,expire_date)
            set_access_cookies(resp, access_token,expire_date)
            login_user(current_user,remember=True)

            return make_response(resp,200)
        else:
            current_user.login_attempts += 1
            db.session.add(current_user)
            db.session.commit()
            return make_response(jsonify({'message':{"success":False,"field":"password","text": 'رمز عبور شما نادرست است'}}),401)

    def get(self):
        return make_response(jsonify({"message":"online resources login"}),404)

class UserLogout(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = Revoked(jti = jti)
            revoked_token.add()
            return make_response(jsonify({'message': 'Access token has been revoked'}),200)
        except Exception as e:
            return make_response(jsonify({'message':{ 'error' : str(e)}}), 500)

class UserLogoutRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = Revoked(jti = jti)
            revoked_token.add()
            return {'message': 'Refresh token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500

class UserTokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity = current_user)
        resp = jsonify({'access_token': access_token})
        resp = jsonify({
            'message': 'Token refreshed for {}'.format(current_user),
            'access_token': access_token,
            })
        set_access_cookies(resp, access_token)
        return make_response(resp,200)

class UserVerification(Resource):
    def put(self):
        if "username" in session:
            current_user = User.find_by_username(session['username'])
            now = datetime.now()
            data = request.get_json(force=True)

            if 'last_send_time' not in session:
                session['last_send_time'] = now + timedelta(seconds=MAX_AVAILABLE_MESSAGE_TIME)

            if 'resend' in data and data['resend']:
                session['last_send_time'] = now + timedelta(seconds=MAX_AVAILABLE_MESSAGE_TIME)

            if (now - session['last_send_time']).seconds >= MAX_AVAILABLE_MESSAGE_TIME:
                if current_user.send_sms_attempts == MAX_MESSAGES_SEND :
                    msg = "حد اکثر تلاشهای شما جهت دریافت کد فعال سازی به اتمام رسیده است. لطفا جهت پیگیری با پشتیبانی سایت تماس حاصل کنید."
                    return make_response(jsonify({"message":{"success":False,"text":msg,"field":"policy"}}),400)

                current_user.activation_code = random.randint(100000,1000000)
                current_user.send_sms_attempts += 1
                current_user.verification_attempts = 0
                db.session.add(current_user)
                db.session.commit()
                session['last_send_time'] = datetime.now()

                text = "فعال سازی حساب کاربری یونی بید" \
                + '\n' + "کدفعال سازی حساب کاربری شما :" \
                + '\n' + current_user.activation_code \
                + '\n' + ' توجه! این کد پس از گذشت ' + str(MAX_AVAILABLE_MESSAGE_TIME) + ' ثانیه منقضی خواهد شد.'\
                + '\n' + 'با آرزوی سلامتی و شادکامی برای شما'\
                + '\n' + 'تیم یونی بید www.unibid.ir'

                SendSMS(current_user.mobile,text)
                return make_response(jsonify({"remained_to_expire": MAX_AVAILABLE_MESSAGE_TIME,"send_attempts":MAX_MESSAGES_SEND - current_user.send_sms_attempts }),200)

            return make_response(jsonify({"remained_to_expire": MAX_AVAILABLE_MESSAGE_TIME - (now - session['last_send_time']).seconds,"send_attempts":MAX_MESSAGES_SEND - current_user.send_sms_attempts }),200)

        msg = "توکن فعال سازی حساب در دسترس نیست. لطفا دوباره اقدام به ورود به سایت کنید."
        return make_response(jsonify({"message":{"success":False,"field":"retry_login","text":msg}}),400)

    def post(self):
        if "username" in session:
            current_user = User.find_by_username(session['username'])

            data = parser_verify.parse_args()
            data = request.get_json(force=True)
            verify_code = data['code']
            now = datetime.now()

            if ((now - current_user.updated_at).seconds >= MAX_DEFFER_ACTIVATION_TIME) and (current_user.verification_attempts == MAX_ACTIVATION_ATTEMPTS):
                current_user.verification_attempts = 0
                db.session.add(current_user)
                db.session.commit()

            if current_user.verification_attempts == MAX_ACTIVATION_ATTEMPTS:
                msg = "حداکثر تلاش های شما در مدت اعتبار کد ارسالی به انجام رسیده است. لطفا مجددا کد فعال سازی خود را درخواست کنید."
                return make_response(jsonify({"message":{"success":False,"text":msg,"field":"policy"}}),400)

            if verify_code != current_user.activation_code:
                current_user.verification_attempts +=1
                db.session.add(current_user)
                db.session.commit()
                msg = "کد وارد شده معتبر نمی باشد"
                return make_response(jsonify({"message":{"success":False,"text":msg,"field":"invalid"}}),400)

            if (now - session['last_send_time']).seconds >= MAX_AVAILABLE_MESSAGE_TIME:
                msg = "کد وارد شده شما منقضی شده است"
                return make_response(jsonify({"message":{"success":False,"text":msg,"field":"expire"}}),400)

            current_user.is_verified = True
            current_user.send_sms_attempts = 0
            current_user.verification_attempts = 0
            current_user.login_attempts = 0
            current_user.is_active = True
            db.session.add(current_user)
            db.session.commit()
            text = "فعال سازی حساب کاربری یونی بید" \
            + '\n' + current_user.username + " عزیز !"\
            + '\n' + "حساب کاربری شما با موفقیت فعال سازی شد" \
            + '\n' + 'ساعات خوشی را برای شما در سایت یونی بید آرزومندیم'\
            + '\n' + 'تیم یونی بید www.unibid.ir'
            SendSMS(current_user.mobile,text)

            access_token = create_access_token(identity = session['username'].lower(),fresh=True,expires_delta=False)
            refresh_token = create_refresh_token(identity = session['username'].lower())

            msg = "حساب کاربری شما با موفقیت فعال شد. لطفا جهت بهبود خدمات نسبت به تکمیل پروفایل کاربری خود اقدام کنید."

            resp = jsonify({
                'text': msg,
                'access_token': access_token,
                'refresh_token': refresh_token
                })

            login_user(current_user,remember=False)
            set_refresh_cookies(resp, refresh_token)
            set_access_cookies(resp, access_token)

            del session['last_send_time']
            del session['username']
            return make_response(resp,200)

        msg = "توکن فعال سازی حساب در دسترس نیست. لطفا دوباره اقدام به ورود به سایت کنید."
        return make_response(jsonify({"message":{"success":False,"field":"retry_login","text":msg}}),400)

    def get(self):
        resp = {
            "message_ttl":MAX_AVAILABLE_MESSAGE_TIME,
        }
        return make_response(jsonify(resp),200)

class UserForgotPassword(Resource):
    def get(self):
        pass
    def post(self):
        parser_forgot.parse_args()

        data = request.get_json(force=True)
        mobile = data.get("mobile", None)

        if User.query.filter_by(mobile=mobile).count() > 1:
            msg = "بیش از یک کاربر با این شماره موبایل در سیستم ثبت شده اند. لطفا جهت پیگیری موضوع با پشتیبانی سایت تماس حاصل کنید."
            return make_response(jsonify({"message":{"success":False,"text":msg,"field":"mobile"}}),400)

        current_user = User.find_by_mobile(mobile)
        if not current_user :
            msg = "کاربری با شماره موبایل وارد شده در سیستم تعریف نشده است"
            return make_response(jsonify({"message":{"success":False,"text":msg,"field":"mobile"}}),400)

        if current_user.send_sms_attempts == MAX_MESSAGES_SEND :
            msg = "حداکثر تلاشهای شما جهت دریافت رمز یکبار مصرف انجام گرفته است. لطفا با پشتیبانی سایت تماس حاصل کنید"
            return make_response(jsonify({"message":{"success":False,"text":msg,"field":"policy"}}),400)


        new_password = str(random.randint(100000,1000000))
        current_user.password =User.generate_hash(new_password)
        current_user.send_sms_attempts += 1
        db.session.add(current_user)
        db.session.commit()
        session['last_send_time'] = datetime.now()

        text = "فراموشی رمز عبور یونی بید" \
        + '\n' + "رمزعبور یکبارمصرف شما در یونی بید :" \
        + '\n' + new_password \
        + '\n' + 'توجه! به لحاظ مسائل امنیتی لطفا پس از اولین ورود به سایت نسبت به تغییر رمز عبور خود اقدام فرمایید'\
        + '\n' + 'با آرزوی سلامتی و شادکامی برای شما'\
        + '\n' + 'تیم یونی بید www.unibid.ir'

        SendSMS(current_user.mobile,text)

        msg = "یک پیام متنی حاوی رمز عبور یکبارمصرف برای شما پیامک شد که به وسیله آن می توانید جهت ورود به سایت اقدام کنید."
        return make_response(jsonify({"message":{"success" : True,"text":msg,"field":"password_sent"}}),200)

class UserChangePassword(Resource):
    @jwt_required
    def post(self):
        parser_change.parse_args()
        data = request.get_json(force=True)

        if not User.verify_hash(data['old_password'], current_user.password):
            return make_response(jsonify({"message":{"success":False,"field":"password","text":'رمز عبور فعلی شما نادرست است'}}),400)


        if len(data['new_password']) > 32 or len(data['new_password']) < 4:
            return make_response(jsonify({"message":{"success":False,"field":"password","text":'رمز عبور جدید شما باید حداقل ۴ و حداکثر ۳۲ کاراکتری باشد'}}),400)

        if(data['new_password']!=data['confirm_password']):
            return make_response(jsonify({"message":{"success":False,"field":"password","text":'تکرار رمزعبور جدید شما با رمز عبور جدید مطابقت ندارد'}}),400)

        current_user.password = User.generate_hash(data['new_password'])
        db.session.add(current_user)
        db.session.commit()

        text = "تغییر رمز عبور حساب کاربری یونی بید" \
        + '\n' + "کاربر گرامی : " + current_user.username \
        + '\n' + 'شما در تاریخ ' + data['current_time'] + 'نسبت به تغییر رمز عبور خود در سایت یونی بید اقدام کرده اید.'\
        + '\n' + 'این پیام صرفا جهت اطلاع رسانی شما ارسال گردیده است.'\
        + '\n' + 'با آرزوی سلامتی و شادکامی برای شما'\
        + '\n' + 'تیم یونی بید www.unibid.ir'

        SendSMS(current_user.mobile,text)
        logout_user()
        return make_response(jsonify({"message":{"success":False,"field":"relogin","text":'رمزعبور شما با موفقیت تغییر کرد.لطفا با استفاده از رمزعبور جدید به سایت وارد شوید.'}}),200)
