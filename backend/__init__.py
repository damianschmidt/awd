from flask import Flask
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    if app.debug:
        CORS(app)

    from backend.api.basic import BASIC
    from backend.api.airport_info import FLIGHT
    from backend.api.weather_info import WEATHER

    app.register_blueprint(BASIC, url_prefix='/api/1')
    app.register_blueprint(FLIGHT, url_prefix='/api/airport')
    app.register_blueprint(WEATHER, url_prefix='/api/weather')

    return app