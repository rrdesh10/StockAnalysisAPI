from flask import Flask
from config import Config
from flask_cors import CORS


def create_app(config_class=Config):
    app=Flask(__name__)
    CORS(app)

    from .routes import api_bp

    app.register_blueprint(api_bp, url_prefix='/api/v1/stocks')


    return app