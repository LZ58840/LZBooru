from flask import request
from flask_restful import abort
from booru.resources.auth_resource import AuthResource

from booru.database import db
from booru.models.dhash import Dhash
from booru.schemas.dhash_schema import DhashSchema

from flask import current_app as app


DHASH_ENDPOINT = "/api/dhash"


class DhashResource(AuthResource):
    """
    A Resource that handles requests related to dhashs.
    """

    def get(self):
        dhashs = Dhash.query.all()
        dhashs_json = [DhashSchema().dump(dhash) for dhash in dhashs]

        app.logger.info(f'"GET {request.full_path}" 200')

        return dhashs_json, 200

    def post(self):
        dhashs = DhashSchema(many=True).load(request.get_json())

        try:
            db.session.add_all(dhashs)
            db.session.commit()

        except Exception as e:
            app.logger.exception(f'"POST {request.full_path}" 500')
            abort(500, message="Unexpected Error!")

        else:
            app.logger.info(f'"POST {request.full_path}" 201')
            return len(dhashs), 201

