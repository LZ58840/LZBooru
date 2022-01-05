import logging
import os

from flask import Flask
from flask_restful import Api

from booru.database import db
from booru.resources.image_resource import IMAGE_ENDPOINT, ImageResource
from booru.resources.link_resource import LINK_ENDPOINT, LinkResource
from booru.resources.submission_resource import SUBMISSION_ENDPOINT, SubmissionResource
from booru.resources.subreddit_resource import SUBREDDIT_ENDPOINT, SubredditResource

from dotenv import dotenv_values


config = dotenv_values(".env")


def create_app():
    """
    Creates the Flask app for LZBooru.

    :return: the created Flask app
    """

    app = Flask(__name__)

    # Configure logging
    disable_werkzeug()
    log_config()

    # Set as SQLite3 by default
    app.logger.info('Configuring database...')
    app.config["SQLALCHEMY_DATABASE_URI"] = config["DATABASE_URI"]
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize database
    app.logger.info('Initializing database...')
    db.init_app(app)

    # Enable foreign key (SQLite3 specific)
    def _fk_pragma_on_connect(dbapi_con, con_record):
        dbapi_con.execute('pragma foreign_keys=ON')

    with app.app_context():
        from sqlalchemy import event
        event.listen(db.engine, 'connect', _fk_pragma_on_connect)
        db.create_all()

    # Initialize routes
    app.logger.info('Configuring endpoints...')
    api = Api(app)
    api.add_resource(SubmissionResource, SUBMISSION_ENDPOINT, f"{SUBMISSION_ENDPOINT}/<url>")
    api.add_resource(ImageResource, IMAGE_ENDPOINT)
    api.add_resource(SubredditResource, SUBREDDIT_ENDPOINT, f"{SUBREDDIT_ENDPOINT}/<name>")
    api.add_resource(LinkResource, LINK_ENDPOINT, f"{LINK_ENDPOINT}/<link_type>")

    app.logger.info('App successfully created. Running...')

    return app


def disable_werkzeug():
    """Disables the default werkzeug logger."""

    logging.getLogger('werkzeug').disabled = True
    os.environ['WERKZEUG_RUN_MAIN'] = 'true'


def log_config():
    """Configures logger with given formatting."""

    root = logging.getLogger()
    handler = root.handlers[0]
    fmt = logging.Formatter(fmt=config["LOG_FMT"], datefmt=config["LOG_DATEFMT"])
    handler.setFormatter(fmt)
