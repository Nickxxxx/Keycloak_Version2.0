from flask import Blueprint, flash, render_template
from blueprints.OIDC_Module import oidc

pages = Blueprint('pages', __name__, template_folder='templates')

@pages.route('/my/Page1')
@oidc.require_login
def Page1():
    flash('Authorized!', 'success')
    return render_template('Page1.html')


#user and Guest
@pages.route('/my/Page2')
@oidc.require_login
def Page2():
    flash('Authorized!', 'success')
    return render_template('Page2.html')


#Page3 user and admin
@pages.route('/my/Page3')
@oidc.require_login
def Page3():
    flash('Authorized!', 'success')
    return render_template('Page3.html')


#Page 4 only admin acess where you can see the admin panel
@pages.route('/my/Page4')
@oidc.require_login
def Page4():
    flash('Authorized!', 'success')
    return render_template('Page4.html')


@pages.route('/my/Admin')
@oidc.require_login
def PageAdmin():
    flash('Authorized!', 'success')
    return render_template('PageAdmin.html')
