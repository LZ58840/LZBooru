from flask import request
from flask_restful import abort
from sqlalchemy.sql import exists
from booru.resources.auth_resource import AuthResource

from booru.database import db
from booru.models.image import Image
from booru.models.histogram import Histogram
from booru.schemas.image_schema import ImageSchema

from flask import current_app as app


IMAGE_ENDPOINT = "/api/image"


class ImageResource(AuthResource):
    """
    A Resource that handles requests related to Images.
    """

    def get(self):
        try:
            quantity = int(request.args.get('q'))

        except (ValueError, TypeError):
            app.logger.info(f'"GET {request.full_path}" 400')
            abort(400, message="Invalid quantity.")

        else:
            images = Image.query.filter(~ exists().where(Image.id == Histogram.id)).limit(quantity).all()
            images_json = [ImageSchema().dump(image) for image in images]

            app.logger.info(f'"GET {request.full_path}" 200')

            return images_json

    def post(self):
        images = ImageSchema(many=True).load(request.get_json())

        try:
            db.session.add_all(images)
            db.session.commit()

        except Exception as e:
            app.logger.exception(f'"POST {request.full_path}" 500')
            abort(500, message="Unexpected Error!")

        else:
            app.logger.info(f'"POST {request.full_path}" 201')
            return len(images), 201

    def delete(self):
        images = ImageSchema(many=True).load(request.get_json())

        try:
            for image in images:
                Image.query.filter_by(id=image.id).delete()

            db.session.commit()
        
        except Exception as e:
            app.logger.exception(f'"DELETE {request.full_path}" 500')
            abort(500, message="Unexpected Error!")

        else:
            app.logger.info(f'"DELETE {request.full_path}" 200')
            return len(images), 200
