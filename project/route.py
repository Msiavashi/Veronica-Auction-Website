# # encoding=utf8
# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')
from project import app
from flask import url_for, redirect, render_template, request, abort
from flask import render_template, jsonify
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import Form, BooleanField, StringField, PasswordField, validators

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
    @app.route('/site/')
    def site():
        return render_template('site/index.html')

    @app.route('/login/')
    def account_login():
        return render_template('site/login.html')

    @app.route('/register/')
    def account_register():
        return render_template('site/register.html')


route = Route()
