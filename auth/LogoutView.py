from flask import Blueprint, redirect, url_for, session

from Oidc_Decorators import oidc

auth = Blueprint('auth', __name__, template_folder='templates')

@auth.route('/logout', methods=['GET', 'POST'])
@oidc.require_login
def logout():
    oidc.logout()
    session.clear()
    return redirect('http://localhost:8080/auth/realms/Application1/protocol/openid-connect/logout?redirect_uri=http://localhost:5000/')


