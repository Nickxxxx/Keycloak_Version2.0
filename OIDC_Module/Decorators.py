import json
from base64 import b64decode
from functools import wraps

from flask import redirect, url_for, flash

from OIDC_Module import oidc


def require_keycloak_role(roles):
    """
        Function to check for a KeyCloak client role in JWT access token.
        This is intended to be replaced with a more generic 'require this value
        in token or claims' system, at which point backwards compatibility will
        be added.
        :param role: A single role or a list of roles that are required. Used to check if the logged_in user has those specific requirements
        :type scopes_required: list or a string
        :returns: True if the specific role was inisde the users realm-settings. 
            An ErrStr (subclass of string for which bool() is False) if
            an error occured.
        :rtype: Boolean or String
    """
    def wrapper(view_func):
        @wraps(view_func)
        def decorated(*args, **kwargs):
            raw_access_token = oidc.get_access_token()
            pre, tkn, post = raw_access_token.split('.')
            access_token = b64decode(tkn + '=' * (-len(tkn) % 4))
            access_token = json.loads(access_token.decode('utf-8'))
            print(raw_access_token)
            print("------")
            print(access_token)
            print("------")
            print(oidc.validate_token(raw_access_token))

            user_id = oidc.user_getfield('sub')
            access_token_id = access_token['sub']

            if oidc.validate_token(raw_access_token) and (user_id == access_token_id):
                for role in roles:
                    if role in access_token['realm_access']['roles']:
                        return view_func(*args, **kwargs)
                else:
                    flash('Unauthorized!', 'danger')
                    return redirect(url_for('dash.dashboard'))
            else:
                flash('Invalid Token!', 'danger')
                return redirect(url_for('dash.dashboard'))
        return decorated
    return wrapper


def validate_accesstoken(f):
    """
        This function can be used to validate tokens.
        Note that this only works if a token introspection url is configured,
        as that URL will be queried for the validity and scopes of a token. 
        The decorator function do not need any parameter since it will get them by itself

        :returns: True if the token was valid and contained the required
            scopes. An ErrStr (subclass of string for which bool() is False) if
            an error occured.
        :rtype: Boolean or String
    """
    @oidc.accept_token(require_token=True)
    @wraps(f)
    def wrap(*args, **kwargs):
        access_token = oidc.get_access_token()
        if oidc.validate_token(access_token):
            return f(*args, **kwargs)
        else:
            flash('Not a valid token', 'danger')
            return redirect(url_for('login'))
    return wrap


'''
def require_login(f):
    """
        This function can be used to validate tokens.
        Note that this only works if a token introspection url is configured,
        as that URL will be queried for the validity and scopes of a token. 
        The decorator function do not need any parameter since it will get them by itself

        :returns: True if the token was valid and contained the required
            scopes. An ErrStr (subclass of string for which bool() is False) if
            an error occured.
        :rtype: Boolean or String
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        if g.oidc_id_token is None:
            return oidc.redirect_to_auth_server(request.url)
        return f(*args, **kwargs)
    return decorated
'''
