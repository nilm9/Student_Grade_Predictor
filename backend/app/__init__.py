from flask import Flask
from flask_cors import CORS
from .api.routes import api_blueprint
from .services.predictions import predictions_blueprint
import os


path = os.path.join(os.path.dirname(__file__), './services/config.py')
def create_app():
    app = Flask(__name__)
    CORS(app)

    app.config.from_pyfile( path)
    app.register_blueprint(api_blueprint, url_prefix='/api')


    return app
