import flask
import flask_restful


class Config:
    DEBUG = False
    TESTING = False
    SECRET_KEY = b">`vK\x11)\xf2\xe9\x03\x08.\x84|)\xf5yX\x81i\xee\xb9h*8"
    APP_NAME = "Enchantments API"
    LOG_FILE = "api.log"


class DevelopmentConfig(Config):
    DEBUG = True
    XSS_ALLOWED_ORIGINS = ["http://localhost:3000", "https://localhost:3000"]


class StatsResource:
    pass


class ApplicationsResource:
    pass


class AwardsResource:
    pass


class ZonesResource:
    pass


def create_app(config_obj=DevelopmentConfig):
    app = flask.Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_obj)
    return app


def initialize(app):
    api = flask_restful.Api(app)

    api.add_resource(StatsResource, "/api/stats", "/api/stats/<obj_id>")
    api.add_resource(ApplicationsResource, "/api/applications", "/api/applications/<obj_id>")
    api.add_resource(AwardsResource, "/api/awards", "/api/awards/<obj_id>")
    api.add_resource(ZonesResource, "/api/zones", "/api/zones/<obj_id>")


app = create_app()
initialize(app)
