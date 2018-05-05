from project import app
from flask import url_for, redirect, render_template, request, abort ,redirect
from flask import render_template, jsonify
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from flask_login import current_user,login_required,logout_user
from .resources import login_manager

# class LoginForm(FlaskForm):
#     username = StringField('نام کاربری', validators=[DataRequired('لطفا نام کاربری خود را وارد کنید')])
#     password = StringField('رمز عبور', validators=[DataRequired('لطفا رمز عبور خود را وارد کنید')])
#
# class RegisterForm(FlaskForm):
#     username = StringField('نام کاربری', validators=[DataRequired('لطفا نام کاربری خود را وارد کنید')])
#     mobile = StringField('تلفن همراه', validators=[DataRequired('لطفا شماره تلفن همراه خود را وارد کنید')])
#     password = PasswordField('رمز عبور', [
#         validators.DataRequired(),
#         validators.EqualTo('c_password', message='رمز عبور با تکرار باید همخوانی داشته باشد')
#     ])
#     c_password = PasswordField('تکرار رمز عبور', validators=[DataRequired('لطفا تکرار رمز عبور خود را وارد کنید')])
#

class Route():
    @app.route('/')
    def site():
        return render_template('site/index.html')

    @app.route('/login/')
    def account_login():
        if current_user.is_authenticated:
            return redirect('/')
        return render_template('site/login.html')

    @app.route('/register/')
    def account_register():
        if current_user.is_authenticated:
            return redirect('/')
        return render_template('site/register.html')

    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        return redirect('/')

    @app.route("/profile")
    @login_required
    def profile():
        return render_template('site/profile.html')

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



route = Route()
