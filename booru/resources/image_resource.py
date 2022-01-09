from flask import request
from flask_restful import abort
from sqlalchemy.exc import IntegrityError
from booru.resources.auth_resource import AuthResource

from booru.database import db
from booru.models.image import Image
from booru.schemas.image_schema import ImageSchema

from flask import current_app as app


IMAGE_ENDPOINT = "/api/image"


class ImageResource(AuthResource):
    """
    A Resource that handles requests related to Images.
    """

    def get(self):
        images = Image.query.all()
        images_json = [ImageSchema().dump(image) for image in images]

        app.logger.info(f'"GET {request.full_path}" 200')

        return images_json, 200

    def post(self):
        images = ImageSchema(many=True).load(request.get_json())

        try:
            db.session.add_all(images)
            db.session.commit()

        except IntegrityError as e:
            app.logger.exception(f'"POST {request.full_path}" 500')
            abort(500, message="Unexpected Error!")

        else:
            app.logger.info(f'"POST {request.full_path}" 201')
            return len(images), 201

