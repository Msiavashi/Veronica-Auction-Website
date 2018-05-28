from markupsafe import Markup
from flask import url_for,render_template,abort,session,redirect
from flask_admin import AdminIndexView
from flask_admin import expose
from flask_login import current_user,login_required
from functools import wraps
from ..middleware import role_admin


class MyAdminIndexView(AdminIndexView):
    @expose('/')
    @role_admin
    def index(self):
        return super(MyAdminIndexView, self).index()
