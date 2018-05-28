from flask_login import current_user,login_required
from functools import wraps
from flask import render_template,abort

def role_admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return render_template('site/login.html')
        found = False
        for role in current_user.roles:
            if( role.name == 'admin' ):
                found = True
                break
        if not found :
            abort(400)
            # return render_template('site/401.html'), 401
        return f(*args, **kwargs)
    return decorated_function

def has_role(user,name):
    found = False
    if(user.is_authenticated):
        for role in user.roles:
            if( role.name == 'admin' ):
                found = True
                break
    return found
