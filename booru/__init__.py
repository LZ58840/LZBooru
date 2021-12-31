from flask import Flask
from flask_restful import Api

from booru.database import db
from booru.resources.image_resource import IMAGE_ENDPOINT, ImageResource
from booru.resources.link_resource import LINK_ENDPOINT, LinkResource
from booru.resources.submission_resource import SubmissionResource, SUBMISSION_ENDPOINT
from booru.resources.subreddit_resource import SUBREDDIT_ENDPOINT, SubredditResource

from dotenv import dotenv_values


def create_app():
    config = dotenv_values(".env")

    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = config["DATABASE_URI"]
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

    # initialize database
    db.init_app(app)

    # Ensure FOREIGN KEY for sqlite3
    def _fk_pragma_on_connect(dbapi_con, con_record):
        dbapi_con.execute('pragma foreign_keys=ON')

    with app.app_context():
        from sqlalchemy import event
        event.listen(db.engine, 'connect', _fk_pragma_on_connect)
        db.create_all()

    # initialize routes
    api = Api(app)
    api.add_resource(SubmissionResource, SUBMISSION_ENDPOINT, f"{SUBMISSION_ENDPOINT}/<url>")
    api.add_resource(ImageResource, IMAGE_ENDPOINT)
    api.add_resource(SubredditResource, SUBREDDIT_ENDPOINT, f"{SUBREDDIT_ENDPOINT}/<name>")
    api.add_resource(LinkResource, LINK_ENDPOINT)

    return app