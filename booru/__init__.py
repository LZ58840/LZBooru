from flask import Flask
from flask_restful import Api

from booru.database import db
from booru.resources.submission_resource import SubmissionResource, SUBMISSION_ENDPOINT
from config import *

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_LOCATION

    # initialize database
    db.init_app(app)
    with app.app_context():
        db.create_all()

    # initialize routes
    api = Api(app)
    api.add_resource(SubmissionResource, SUBMISSION_ENDPOINT, f"{SUBMISSION_ENDPOINT}/<id>")

    return app