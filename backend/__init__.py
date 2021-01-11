from flask import Flask
from flask_cors import CORS


def create_app():
    app = Flask(__name__)

    from backend.api.basic import BASIC
    from backend.api.airport_info import FLIGHT

    app.register_blueprint(BASIC, url_prefix='/api/1')
    app.register_blueprint(FLIGHT, url_prefix='/api/airport')

    return app
