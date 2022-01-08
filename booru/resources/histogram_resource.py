from flask import request
from flask_restful import abort
from booru.resources.auth_resource import AuthResource

from booru.database import db
from booru.models.histogram import Histogram
from booru.schemas.histogram_schema import HistogramSchema

from flask import current_app as app


HISTOGRAM_ENDPOINT = "/api/histogram"


class HistogramResource(AuthResource):
    """
    A Resource that handles requests related to histograms.
    """

    def get(self):
        histograms = Histogram.query.all()
        histograms_json = [HistogramSchema().dump(histogram) for histogram in histograms]

        app.logger.info(f'"GET {request.full_path}" 200')

        return histograms_json, 200

    def post(self):
        histograms = HistogramSchema(many=True).load(request.get_json())

        try:
            db.session.add_all(histograms)
            db.session.commit()

        except Exception as e:
            app.logger.exception(f'"POST {request.full_path}" 500')
            abort(500, message="Unexpected Error!")

        else:
            app.logger.info(f'"POST {request.full_path}" 201')
            return len(histograms), 201

