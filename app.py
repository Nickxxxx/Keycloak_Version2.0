from flask import Flask
from flask.globals import current_app
from flask_oidc import OpenIDConnect


# Import parts of our application


def init_app():
    """Create Flask application."""
    app = Flask(__name__, static_folder='static', static_url_path='')
    app.config.from_object('config.Config')

    with app.app_context():
        from Startscreen.StartView import start
        from auth.LogoutView import auth
        from Home.DashboardView import dash
       
        
        # Register Blueprints
        app.register_blueprint(start)
        app.register_blueprint(auth)
        app.register_blueprint(dash)

        return app


def init_oidc():
    oidc = OpenIDConnect(current_app)
    return oidc


if __name__ == "__main__":
    app = init_app()
    app.run()
