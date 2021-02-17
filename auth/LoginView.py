from flask import Blueprint, redirect, url_for, session

from OIDC_Module import oidc

auth = Blueprint('auth', __name__, template_folder='templates')


@auth.route('/login', methods=['GET', 'POST'])
@oidc.require_login
def login():
    print("Hello")
    return redirect(url_for('dash.dashboard'))


@auth.route('/protected/logout', methods=['GET'])
@oidc.require_login
def logout():
    oidc.logout()
    session.clear()
    return redirect('http://localhost:8080/auth/realms/Application1/protocol/openid-connect/logout?redirect_uri=http://localhost:5000/')

#Reihenfolge der Routen spielt eine Rolle!
