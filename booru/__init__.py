import logging
import os

from flask import Flask
from flask_restful import Api
from sqlalchemy import text

from booru.database import ABS_NORM_FUNC, DHASH_XOR_FUNC, EUCL_NORM_FUNC, db
from booru.resources.dhash_resource import DHASH_ENDPOINT, DhashResource
from booru.resources.histogram_resource import HISTOGRAM_ENDPOINT, HistogramResource
from booru.resources.image_resource import IMAGE_ENDPOINT, ImageResource
from booru.resources.link_resource import LINK_ENDPOINT, LinkResource
from booru.resources.similarity_resource import SIMILARITY_ENDPOINT, SimilarityResource
from booru.resources.submission_resource import SUBMISSION_ENDPOINT, SubmissionResource
from booru.resources.subreddit_resource import SUBREDDIT_ENDPOINT, SubredditResource

from tools.loggers.singleproc_logger import log_config

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

    app.logger.info('Configuring database...')
    app.config["SQLALCHEMY_DATABASE_URI"] = config["DATABASE_URI"]
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize database
    app.logger.info('Initializing database...')
    db.init_app(app)

    # # Enable foreign key (SQLite3 specific)
    # def _fk_pragma_on_connect(dbapi_con, con_record):
    #     dbapi_con.execute('pragma foreign_keys=ON')

    with app.app_context():
        # event.listen(db.engine, 'connect', _fk_pragma_on_connect)
        db.create_all()
        with db.engine.connect() as con:
            con.execute(text(ABS_NORM_FUNC))
            con.execute(text(EUCL_NORM_FUNC))
            con.execute(text(DHASH_XOR_FUNC))


    # Initialize routes
    app.logger.info('Configuring endpoints...')
    api = Api(app)
    api.add_resource(SubmissionResource, SUBMISSION_ENDPOINT, f"{SUBMISSION_ENDPOINT}/<url>")
    api.add_resource(ImageResource, IMAGE_ENDPOINT)
    api.add_resource(HistogramResource, HISTOGRAM_ENDPOINT)
    api.add_resource(DhashResource, DHASH_ENDPOINT)
    api.add_resource(SubredditResource, SUBREDDIT_ENDPOINT, f"{SUBREDDIT_ENDPOINT}/<name>")
    api.add_resource(LinkResource, LINK_ENDPOINT, f"{LINK_ENDPOINT}/<link_type>")
    api.add_resource(SimilarityResource, SIMILARITY_ENDPOINT, f"{SIMILARITY_ENDPOINT}/<source>")

    app.logger.info('App successfully created. Running...')

    return app


def disable_werkzeug():
    """Disables the default werkzeug logger."""

    logging.getLogger('werkzeug').disabled = True
    os.environ['WERKZEUG_RUN_MAIN'] = 'true'
