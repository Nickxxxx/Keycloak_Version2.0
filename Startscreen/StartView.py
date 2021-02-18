from flask import Blueprint, flash, redirect, url_for

from Oidc_Decorators import oidc

start = Blueprint('home', __name__, template_folder='templates')

@start.route('/')
def Startscreen():
    if oidc.user_loggedin:
        flash('Welcome %s' % oidc.user_getfield('username'))
        return redirect(url_for('dash.dashboard'))
    else:
        return 'Welcome anonymous, <a href="/my">Log in</a>'
