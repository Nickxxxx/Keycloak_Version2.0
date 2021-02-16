import json
from base64 import b64decode

import requests
from flask import Blueprint, render_template, redirect, url_for, flash, session
from oauth2client.client import OAuth2Credentials

from OIDC_Module import oidc

dash = Blueprint('dash', __name__, template_folder='templates')


@dash.route('/my/', methods=['POST', 'GET'])
@oidc.require_login
def dashboard():
    if oidc.user_loggedin:
        info = oidc.user_getinfo(
            ['preferred_username', 'email', 'sub'])

        name = info.get('preferred_username')
        email = info.get('email')
        user_id = info.get('sub')

        response = requests.get(
            'http://localhost:8080/auth/realms/Application1/users/6ceaf804-e731-4415-9754-6411f89120a4/sessions')
        print(response)

        if user_id in oidc.credentials_store:

            access_token = OAuth2Credentials.from_json(
                oidc.credentials_store[user_id]).access_token
            #print('access_token=<%s>' % access_token)
            headers = {'Authorization': 'Bearer %s' % (access_token)}

            flash('Welcome %s' % oidc.user_getfield(
                'preferred_username'), 'success')
            return render_template('main.html', name=name)

        else:
            session.clear()
            oidc.logout()
            return redirect('http://localhost:8080/auth/realms/Application1/protocol/openid-connect/logout?redirect_uri=http://localhost:5000/')

    return redirect(url_for('auth.login'))


@dash.route('/my/AccessToken')
@oidc.require_login
def showAccessToken():
    if oidc.user_loggedin:
        info = oidc.user_getinfo(['sub'])
        user_id = info.get('sub')

        if user_id in oidc.credentials_store:

            access_token = OAuth2Credentials.from_json(
                oidc.credentials_store[user_id]).access_token
            pre, tkn, post = access_token.split('.')
            access_token_part2 = b64decode(tkn + '=' * (-len(tkn) % 4))
            access_token_part2 = json.loads(access_token_part2.decode('utf-8'))

            return access_token_part2
        else:
            session.clear()
            oidc.logout()
            return redirect('http://localhost:8080/auth/realms/Application1/protocol/openid-connect/logout?redirect_uri=http://localhost:5000/')

    return redirect(url_for('auth.login'))
