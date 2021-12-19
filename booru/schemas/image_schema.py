from marshmallow import Schema, fields, post_load
from booru.models.image import Image


class ImageSchema(Schema):
    id = fields.Integer()
    url = fields.String(allow_none=False)

    @post_load
    def make_image(self, data, **kwargs):
        return Image(**data)