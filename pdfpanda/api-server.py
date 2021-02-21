import math
import pdb
import csv
import flask
import flask_restful
from sqlalchemy import create_engine, Column, Integer, String, MetaData, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import Date
from sqlalchemy.orm import sessionmaker
from dataclasses import dataclass

SQLALCHEMY_DATABASE_URL = "sqlite:///./enchantments.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
meta = MetaData()


@dataclass
class Zone(Base):
    __tablename__ = "zones"
    zone_id: int
    name: str

    zone_id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

    def jsonify(self):
        return {self.zone_id: {"zone_id": self.zone_id, "name": self.name}}


@dataclass
class Award(Base):
    __tablename__ = "awards"
    award_id: int
    application_id: int
    zone_id: int
    pref: int
    entry: str
    size: int

    award_id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer)
    zone_id = Column(Integer)
    pref = Column(Integer)
    entry = Column(String)
    size = Column(Integer)

    def jsonify(self):
        return {
            self.award_id: {
                "award_id": self.award_id,
                "application_id": self.application_id,
                "zone_id": self.zone_id,
                "pref": self.pref,
                "entry": self.entry,
                "size": self.size,
            }
        }


@dataclass
class Application(Base):
    __tablename__ = "applications"

    application_id: int
    date1: str
    date2: str
    date3: str
    zone1: int
    zone2: int
    zone3: int
    awarded: bool

    application_id = Column(Integer, primary_key=True, index=True)
    date1 = Column(String)
    date2 = Column(String)
    date3 = Column(String)
    zone1 = Column(Integer)
    zone2 = Column(Integer)
    zone3 = Column(Integer)
    awarded = Column(Boolean)
    award_id = Column(Integer)

    def jsonify(self):
        return {
            self.application_id: {
                "application_id": self.application_id,
                "date1": self.date1,
                "date2": self.date2,
                "date3": self.date3,
                "zone1": self.zone1,
                "zone2": self.zone2,
                "zone3": self.zone3,
                "awarded": self.awarded,
                "award_id": self.award_id,
            }
        }


Base.metadata.create_all(engine)


def create_db():
    db = SessionLocal()
    # c.execute(
    #     """create table applications
    # (id integer, date1 varchar, date2 varchar, date3 varchar, zone1 integer, zone2 integer, zone3 integer, awarded boolean)"""
    # )

    # c.execute(
    #     """create table awards
    # (id integer, application integer, pref integer, entry varchar, zone integer, size integer)"""
    # )

    zones = [
        "",
        "Colchuck Zone",
        "Core Enchantment Zone",
        "Eightmile/Caroline Zone",
        "Stuart  Zone",
        "Snow Zone",
        "Stuart Zone (stock)",
        "Eightmile/Caroline Zone (",
        "Eightmile/Caroline Zone (stock)",
    ]

    db.query(Zone).delete()
    for id in range(1, len(zones)):
        record = Zone(
            zone_id=id,
            name=zones[id],
        )
        db.add(record)
    db.commit()

    with open("pdfpanda/cleaned.csv", encoding="utf-8") as csvf:
        csvReader = csv.DictReader(csvf)

        db.query(Award).delete()
        db.query(Application).delete()
        app_id = 0
        award_id = 0
        for row in csvReader:
            zone1 = zones.index(row["zone1"])
            zone2 = zones.index(row["zone2"])
            zone3 = zones.index(row["zone3"])
            awarded = True if row["awarded"] == "Awarded" else False
            app_id += 1
            award_id_or_none = -1
            if awarded:
                award_id += 1
                awarded_zone = zones.index(row["awardZone"])
                record = Award(
                    award_id=award_id,
                    application_id=app_id,
                    zone_id=awarded_zone,
                    pref=row["awardPref"],
                    entry=row["awardDate"],
                    size=row["awardSize"],
                )
                db.add(record)
                db.commit()
                award_id_or_none = award_id
            record = Application(
                application_id=app_id,
                date1=row["date1"],
                date2=row["date2"],
                date3=row["date3"],
                zone1=zone1,
                zone2=zone2,
                zone3=zone3,
                awarded=awarded,
                award_id=award_id_or_none,
            )
            db.add(record)
            db.commit()


class Config:
    DEBUG = False
    TESTING = False
    SECRET_KEY = b">`vK\x11)\xf2\xe9\x03\x08.\x84|)\xf5yX\x81i\xee\xb9h*8"
    APP_NAME = "Enchantments API"
    LOG_FILE = "api.log"


class DevelopmentConfig(Config):
    DEBUG = True
    XSS_ALLOWED_ORIGINS = ["http://localhost:3000", "https://localhost:3000"]


def sa_to_json(sa_obj):
    if type(sa_obj) is list:
        return {"data": [dc_obj.jsonify() for dc_obj in sa_obj]}
    return sa_obj.jsonify()


def page_to_json(sa_obj, pagination):
    data = sa_to_json(sa_obj)
    return {"data": data["data"], "pagination": pagination}


class StatsResource(flask_restful.Resource):
    pass


class ApplicationsResource(flask_restful.Resource):
    def get(self, obj_id: str = None):
        params = flask.request.args
        page = int(params.get("page")) if params.get("page") else 0
        limit = int(params.get("limit")) if params.get("limit") else 100
        if limit > 1000:
            limit = 1000
        if limit < 1:
            limit = 1
        offset = page * limit
        db = SessionLocal()
        Base.metadata.create_all(bind=engine)
        if obj_id:
            sa_obj = db.query(Application).filter_by(zone_id=obj_id).first()
        else:
            sa_obj = db.query(Application).limit(limit).offset(offset).all()
            total_records = db.query(Application).count()
            total_pages = math.ceil(total_records / limit)
            has_next = page < total_pages
            has_previous = page > 0
            next_page = f"/api/applications?page={page+1}&limit={limit}" if has_next else False
            previous_page = f"/api/applications?page={page-1}&limit={limit}" if has_previous else False
            pagination = {
                "page": page,
                "limit": limit,
                "offset": offset,
                "total_pages": total_pages,
                "total_records": total_records,
                "has_next": has_next,
                "has_previous": has_previous,
                "next_page": next_page,
                "previous_page": previous_page,
            }
        return page_to_json(sa_obj, pagination), 200


class AwardsResource(flask_restful.Resource):
    def get(self, obj_id: str = None):
        params = flask.request.args
        page = int(params.get("page")) if params.get("page") else 0
        limit = int(params.get("limit")) if params.get("limit") else 100
        if limit > 1000:
            limit = 1000
        if limit < 1:
            limit = 1
        offset = page * limit
        db = SessionLocal()
        Base.metadata.create_all(bind=engine)
        if obj_id:
            sa_obj = db.query(Award).filter_by(zone_id=obj_id).first()
        else:
            sa_obj = db.query(Award).limit(limit).offset(offset).all()
            total_records = db.query(Award).count()
            total_pages = math.ceil(total_records / limit)
            has_next = page < total_pages
            has_previous = page > 0
            next_page = f"/api/awards?page={page+1}&limit={limit}" if has_next else False
            previous_page = f"/api/awards?page={page-1}&limit={limit}" if has_previous else False
            pagination = {
                "page": page,
                "limit": limit,
                "offset": offset,
                "total_pages": total_pages,
                "total_records": total_records,
                "has_next": has_next,
                "has_previous": has_previous,
                "next_page": next_page,
                "previous_page": previous_page,
            }
        return page_to_json(sa_obj, pagination), 200


class ZonesResource(flask_restful.Resource):
    def get(self, obj_id: str = None):
        db = SessionLocal()
        Base.metadata.create_all(bind=engine)
        if obj_id:
            sa_obj = db.query(Zone).filter_by(zone_id=obj_id).first()
        else:
            sa_obj = db.query(Zone).all()
        return sa_to_json(sa_obj), 200


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


# create_db()
app = create_app()
initialize(app)


# Notes:
# To create the sqlite database file (enchantments.db) - make sure it doesn't exist or delete it if it does
# Uncomment create_db()
# coment create_app and initialize(app)
# run:  pipenv run python pdfpanda/api-server.py from repo root
#
# To run the flask app, comment create_db(), uncomment create_app and initialize(app)
# Set the env vars:
# FLASK_APP=pdfpanda.api-server
# FLASK_ENV=development
# FLASK_PORT=5000
# FLASK_HOST=localhost
# run: pipenv run flask run --host $FLASK_HOST --port $FLASK_PORT
