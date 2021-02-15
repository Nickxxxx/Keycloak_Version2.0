from flask import Blueprint, request, flash, redirect, url_for
from blueprints.OIDC_Module import oidc

home = Blueprint('home', __name__, template_folder='templates')

@home.route('/')
def start():
    test = request.headers.get('User-Agent')
    print(test)
    if oidc.user_loggedin:
        flash('Welcome %s' % oidc.user_getfield('username'))
        return redirect(url_for('dash.dashboard'))
    else:
        return 'Welcome anonymous, <a href="/login">Log in</a>'
