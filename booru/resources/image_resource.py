from flask import request
from flask_restful import abort
from sqlalchemy.exc import IntegrityError
from booru.resources.auth_resource import AuthResource

from booru.database import db
from booru.models.image import Image
from booru.schemas.image_schema import ImageSchema


IMAGE_ENDPOINT = "/api/image"


class ImageResource(AuthResource):
    def get(self):
        images = Image.query.all()
        images_json = [ImageSchema().dump(image) for image in images]
        return images_json, 200

    def post(self):
        image = ImageSchema().load(request.get_json())

        try:
            db.session.add(image)
            db.session.commit()
        except IntegrityError as e:
            abort(500, message="Unexpected Error!")
        else:
            return image.id, 201

