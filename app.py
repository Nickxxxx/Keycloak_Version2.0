from flask import Flask
from flask.globals import current_app
from flask_oidc import OpenIDConnect


# Import parts of our application


def init_app():
    """Create Flask application."""
    app = Flask(__name__, static_folder='static', static_url_path='')
    app.config.update({
                          'SECRET_KEY': 'u\x91\xcf\xfa\x0c\xb9\x95\xe3t\xba2K\x7f\xfd\xca\xa3\x9f\x90\x88\xb8\xee\xa4\xd6\xe4',
                          'OIDC_CLIENT_SECRETS': '.\client_secrets.json',
                          'OIDC_ID_TOKEN_COOKIE_SECURE': False,
                          'OIDC_VALID_ISSUERS': ['http://localhost:8080/auth/realms/Application1'],
                          'OIDC_SCOPES': ['openid', 'email', 'profile'],
                          'OIDC_INTROSPECTION_AUTH_METHOD': 'client_secret_post',
                          'OIDC_RESOURCE_CHECK_AUD': True,  # Audience
                          'OIDC_CLOCK_SKEW': 560
                          })

    with app.app_context():
        from auth.LoginView import auth
        from Dashboard.DashboardView import dash
        from home.HomeView import home
        from pages.PageViews import pages
        # Register Blueprints
        app.register_blueprint(home)
        app.register_blueprint(auth)
        app.register_blueprint(dash)
        app.register_blueprint(pages)

        return app


def init_oidc():
    oidc = OpenIDConnect(current_app)
    return oidc


if __name__ == "__main__":
    app = init_app()
    app.run()
