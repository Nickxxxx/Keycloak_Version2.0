from flask import Flask
from flask.globals import current_app
from flask_oidc import OpenIDConnect


def init_app():
    """Create Flask application."""
    app = Flask(__name__)
    app.config.update({
        'SECRET_KEY': 'u\x91\xcf\xfa\x0c\xb9\x95\xe3t\xba2K\x7f\xfd\xca\xa3\x9f\x90\x88\xb8\xee\xa4\xd6\xe4',
        'OIDC_CLIENT_SECRETS': 'C:\VisualStudio\Flask-Keycloak\client_secrets.json',
        'OIDC_CALLBACK_ROUTE': '/callback',
        'OIDC_VALID_ISSUERS': ['http://localhost:8080/auth/realms/Application1'],
        'OIDC_SCOPES': ['openid', 'email', 'profile']
    })

    with app.app_context():
        # Import parts of our application
        from blueprints.Home.HomeView import home
        from blueprints.Auth.loginView import auth
        from blueprints.Dashboard.dashboardView import dash
        from blueprints.Pages.PageViews import pages

        # Register Blueprints
        app.register_blueprint(home)
        app.register_blueprint(auth)
        app.register_blueprint(dash)
        app.register_blueprint(pages)

        return app

        
def init_oidc():
    oidc = OpenIDConnect(current_app)
    return oidc
