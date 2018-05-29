from flask import Flask
from .models import db, migrate


def create_app(mode):
    """Application factory, used to create application
    """
    app = Flask(__name__)
    app.config.from_object('settings.' + mode)

    register_blueprints(app)
    register_extentions(app)
    return app


def register_blueprints(app):

    # Client endpoints
    from app.client import client as client_bp
    app.register_blueprint(client_bp)

    # API endpoints
    from app.api import api as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    return


def register_extentions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    return
